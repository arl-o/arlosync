import argparse
import asyncio
import collections
import functools
import hashlib
import io
import itertools
import logging
import pathlib
import sys
from typing import (
    AbstractSet,
    AsyncIterable,
    BinaryIO,
    Callable,
    Iterable,
    NewType,
    Tuple,
)

import grpc
import sortedcontainers

from arlosync import file_helpers
from arlosync.adler import adler32
from arlosync.protos import arlosync_pb2, arlosync_pb2_grpc

_BytesAndTokens = arlosync_pb2.BytesAndTokens
_FileAndTokens = arlosync_pb2.FileAndTokens
_HashTokens = arlosync_pb2.HashTokens


parser = argparse.ArgumentParser(description="File sync client.")
parser.add_argument("dir", type=str, help="Path of directory to sync to the server.")
parser.add_argument(
    "--port",
    default=50051,
    type=int,
    help=("Client port."),
)


IsToken = NewType("IsToken", bool)

DEFAULT_GROUP_SIZE_BYTES = 4096


def group_tokens_and_literal_bytes(
    func: Callable[..., Tuple[IsToken, bytes]],
    hash_size_bytes: int = 32,
    group_size_bytes: int = DEFAULT_GROUP_SIZE_BYTES,
) -> Callable[..., Iterable[_BytesAndTokens]]:
    """Groups the output `func` into BytesAndTokens protos of size `group_size_bytes`."""

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        for is_token, yielded in itertools.groupby(
            func(*args, **kwargs), lambda x: x[0]
        ):
            slice_size = (
                max(1, round(group_size_bytes / hash_size_bytes))
                if is_token
                else group_size_bytes
            )
            while grouped := tuple(b[1] for b in itertools.islice(yielded, slice_size)):
                if is_token:
                    yield _BytesAndTokens(hash_tokens=_HashTokens(tokens=grouped))
                else:
                    yield _BytesAndTokens(literal_bytes=b"".join(grouped))

    return wrapped


@group_tokens_and_literal_bytes
def get_interleaved_tokens_and_literal_bytes(
    contents: BinaryIO,
    server_chunk_hashes: AbstractSet[bytes],
    server_chunk_checksums: AbstractSet[int],
    file_chunk_size: int,
) -> Iterable[_BytesAndTokens]:
    """Yields literal bytes, or hash tokens for chunks of size file_chunk_size.

    This function is a good candidate for optimization, e.g. with numba or
     calling out to a lower-level language.

    Args:
      contents: Binary IO with the `.read` method. Raises a ValueError if the
          input is a closed file and this function has not finished yielding.
      server_chunk_hashes: Fast-lookup container for blake2s hashes. Used as
          tokens to tell the server to re-use existing data.
      server_chunk_checksums: Fast-lookup container for adler32 checksums. Used
          as a filter, full blake2s hashes are only computed if a checksum
          matches.
      file_chunk_size: Size of file chunks to compare against hashes.
    """
    # Shortcut if there's no point to hashing.
    if not server_chunk_hashes:
        while out_ord := contents.read(1):
            yield IsToken(False), out_ord
        return

    chunk_queue = collections.deque(contents.read(file_chunk_size))
    rolling_checksum = adler32(bytes(chunk_queue))

    while chunk_queue:
        if (
            rolling_checksum.digest() in server_chunk_checksums
            and (hash := hashlib.blake2s(bytes(chunk_queue)).digest())
            in server_chunk_hashes
        ):
            yield IsToken(True), hash
            chunk_queue = collections.deque(contents.read(file_chunk_size))
            rolling_checksum = adler32(bytes(chunk_queue))
        else:
            out_ord = chunk_queue.popleft()
            yield IsToken(False), out_ord.to_bytes(1, sys.byteorder)
            for in_ord in contents.read(1):
                chunk_queue.append(in_ord)
                rolling_checksum.update(in_ord, out_ord)


class SyncClientServicer(arlosync_pb2_grpc.SyncClient):
    def __init__(self, dir: pathlib.Path):
        super().__init__()
        self.dir = dir

    async def GetBytesAndTokensForDirectoryDescriptor(
        self,
        request: _FileAndTokens,
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterable[_BytesAndTokens]:
        """Return bytes and tokens which can reconstrict directory metadata."""
        directory_descriptor = file_helpers.build_directory_descriptor(self.dir)
        for response in get_interleaved_tokens_and_literal_bytes(
            io.BytesIO(directory_descriptor.SerializeToString()),
            set(request.hash_tokens),
            set(request.checksums),
            request.chunk_size,
        ):
            yield response

    async def GetBytesAndTokensForFile(
        self,
        request: _FileAndTokens,
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterable[_BytesAndTokens]:
        """Return bytes and tokens which can reconstruct the specified file.

        Returns status code `NOT_FOUND` if the file is not in the client
        directory.
        """
        absolute_path = self.dir / pathlib.Path(request.path)
        logging.info(f"Starting serving '{request.path}'.")
        if not absolute_path.exists():
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"File '{request.path}' not found.",
            )
        file_size_bytes = absolute_path.stat().st_size
        with absolute_path.open("rb") as in_file:
            for response in get_interleaved_tokens_and_literal_bytes(
                in_file,
                set(request.hash_tokens),
                set(request.checksums),
                request.chunk_size,
            ):
                yield response
        logging.info(f"Finished serving '{request.path}'.")


async def serve(server: SyncClientServicer, port: int) -> None:
    port = server.add_insecure_port(f"localhost:{port}")
    logging.info(f"Starting client on '{port}'.")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    server = grpc.aio.server(compression=grpc.Compression.Gzip)
    arlosync_pb2_grpc.add_SyncClientServicer_to_server(
        SyncClientServicer(pathlib.Path(args.dir)), server
    )
    asyncio.get_event_loop().run_until_complete(serve(server, args.port))
