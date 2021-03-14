import argparse
import asyncio
import contextlib
import hashlib
import io
import logging
import pathlib
from typing import (
    AsyncIterable,
    BinaryIO,
    Callable,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
)

import grpc
import sortedcontainers

from arlosync import file_helpers
from arlosync.adler import adler32
from arlosync.protos import arlosync_pb2, arlosync_pb2_grpc

_DirectoryDescriptor = arlosync_pb2.DirectoryDescriptor
_FileDescriptor = arlosync_pb2.FileDescriptor
_FileAndTokens = arlosync_pb2.FileAndTokens
_BytesAndTokens = arlosync_pb2.BytesAndTokens


parser = argparse.ArgumentParser(description="File sync server.")
parser.add_argument(
    "dir", type=str, help="Path of directory to keep in sync with the client."
)
parser.add_argument(
    "--fuzziness",
    default=1,
    type=int,
    help=(
        "Size of fuzzy lookaround for candidate files. "
        "Default 1, set to 0 for no lookaround."
    ),
)
parser.add_argument(
    "--sync_wait_sec",
    # For small directory descriptors, 5s uses about 600kB up/down per day.
    default=5.0,
    type=float,
    help=("Time to wait between sync events, default 5s."),
)
parser.add_argument(
    "--port",
    default=50051,
    type=int,
    help=("Client port."),
)


class SyncServer:
    def __init__(
        self,
        dir: pathlib.Path,
        fuzziness: int,
        stub: arlosync_pb2_grpc.SyncClientStub,
    ):
        self.dir = dir
        self.fuzziness = fuzziness
        self.stub = stub

        # Cache of most recent client directory description.
        self._client_directory_descriptor = _DirectoryDescriptor()

    async def sync_directory(self) -> None:
        """Syncs `self.dir` with the directory of the client via `self.stub`.

        Creates client directories, syncs files in those directories, and cleans
        up any files or directories no longer found in the client.
        """
        prev_client_directory_descriptor = self._client_directory_descriptor
        client_directory_descriptor = await self._update_client_directory_descriptor()
        # Set up directories.
        for subdir in client_directory_descriptor.sub_directories:
            (self.dir / pathlib.Path(subdir)).mkdir(parents=True, exist_ok=True)

        # Prepare view of local files for fuzzy lookaround.
        local_file_descriptors_by_size = sortedcontainers.SortedList(
            file_helpers.build_directory_descriptor(self.dir).file_descriptors,
            key=lambda d: d.filesize,
        )
        client_previous_mtime_by_path = {
            f_d.path: f_d.mtime
            for f_d in prev_client_directory_descriptor.file_descriptors
        }
        # Set up coroutines for syncing necessary files, and find relevant
        # local files.
        file_resolvers = []
        for client_file_descriptor in filter(
            lambda f_d: self._needs_to_sync(f_d, client_previous_mtime_by_path),
            client_directory_descriptor.file_descriptors,
        ):
            path = pathlib.Path(client_file_descriptor.path)
            if (self.dir / path).exists():
                relevant_files = [path]
            else:
                relevant_files = self._fuzzy_find_relevant_files(
                    local_file_descriptors_by_size, client_file_descriptor.filesize
                )
            file_resolvers.append(self.sync_file(path, relevant_files))

        # Sync the files, and clean up the directory.
        await asyncio.gather(*file_resolvers)
        self._clean_up_directory(client_directory_descriptor)

    async def sync_file(
        self,
        file: pathlib.Path,
        relevant_files: List[pathlib.Path],
    ) -> None:
        """Syncronizes the given file with the version in the client.

        Args:
            file: The relative file path in both server and client directories.
                Server version will be created if it does not exist.
            relevant_files: Relative paths of files which may overlap with the
                expected contents of the updated file. Hash tokens are generated
                from these files. Can contain `file`. All files must exist.
        """
        chunk_size = (
            file_helpers.get_optimal_chunk_size(
                (self.dir / relevant_files[len(relevant_files) // 2]).stat().st_size,
            )
            if relevant_files
            else 1
        )
        logging.info(f"Starting sync of '{file}'.")
        with contextlib.ExitStack() as context:
            request, contents_by_hash_token = self._preprocess_for_sync(
                [
                    context.enter_context((self.dir / path).open("rb"))
                    for path in relevant_files
                ],
                chunk_size,
                str(file),
            )
        try:
            with (self.dir / file).open("wb") as outfile:
                await self._process_sync_response(
                    self.stub.GetBytesAndTokensForFile(request),
                    contents_by_hash_token,
                    outfile,
                    str(file),
                )
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                logging.warning(
                    f"Client could not find file '{file}', server view of "
                    "client directory may be out of date."
                )
            else:
                raise

    async def _update_client_directory_descriptor(self) -> None:
        """Uses the sync algorithm to return a view of the client directory.

        For large-N of files, the overhead of transferring metadata about the
        client's directory (filenames, file sizes) dominates the overall network
        usage. We use the same sync algorithm we use for files to sync this
        metadata to alleviate this case.

        Also updates self._client_directory_descriptor.
        """
        binary_dir_descriptor = self._client_directory_descriptor.SerializeToString()
        request, contents_by_hash_token = self._preprocess_for_sync(
            [io.BytesIO(binary_dir_descriptor)],
            file_helpers.get_optimal_chunk_size(
                len(binary_dir_descriptor), num_expected_untokenized_chunks=0.05
            ),
        )
        out_bytes = io.BytesIO()
        await self._process_sync_response(
            self.stub.GetBytesAndTokensForDirectoryDescriptor(request),
            contents_by_hash_token,
            out_bytes,
        )
        self._client_directory_descriptor = _DirectoryDescriptor.FromString(
            out_bytes.getvalue()
        )
        return self._client_directory_descriptor

    def _preprocess_for_sync(
        self,
        in_bytes_iter: Iterable[BinaryIO],
        chunk_size: int,
        file_path: Optional[str] = None,
    ) -> Tuple[_FileAndTokens, Mapping[bytes, bytes]]:
        """Return a _FileAndTokens request, and chunks of the input indexed by hash."""
        contents_by_hash_token, checksums = {}, set()
        for in_bytes in in_bytes_iter:
            while chunk := in_bytes.read(chunk_size):
                contents_by_hash_token[hashlib.blake2s(chunk).digest()] = chunk
                checksums.add(adler32(chunk).digest())
        return (
            _FileAndTokens(
                path=file_path,
                checksums=checksums,
                hash_tokens=contents_by_hash_token.keys(),
                chunk_size=chunk_size,
            ),
            contents_by_hash_token,
        )

    async def _process_sync_response(
        self,
        response: AsyncIterable[_BytesAndTokens],
        contents_by_hash_token: Mapping[bytes, bytes],
        out_bytes: BinaryIO,
        logging_id: Optional[str] = None,
    ) -> None:
        """Process the response by writing the literal and implied (by hash) contents."""
        num_bytes_local, num_bytes_from_client = 0, 0
        async for bytes_or_tokens in response:
            num_bytes_from_client += out_bytes.write(bytes_or_tokens.literal_bytes)
            for token in bytes_or_tokens.hash_tokens.tokens:
                num_bytes_local += out_bytes.write(contents_by_hash_token[token])

        # Log the result.
        if logging_id:
            if not (total_bytes := num_bytes_local + num_bytes_from_client):
                logging.info(f"Synced '{logging_id}', 0 bytes.")
            else:
                logging.info(
                    f"Synced '{logging_id}', "
                    f"found {num_bytes_local/total_bytes:.0%} "
                    f"of {total_bytes} bytes locally."
                )

    def _fuzzy_find_relevant_files(
        self,
        file_descriptors_by_size: sortedcontainers.SortedList[_FileDescriptor],
        file_size_bytes: int,
    ) -> List[pathlib.Path]:
        """Return N(=fuzziness) local files nearest in size to `file_size_bytes`."""
        index_nearest_filesize = file_descriptors_by_size.bisect(
            _FileDescriptor(filesize=file_size_bytes)
        )
        N = self.fuzziness
        lower_bound = int(max(0, index_nearest_filesize - N / 2))
        upper_bound = int(index_nearest_filesize + N / 2)
        return [
            pathlib.Path(f.path)
            for f in file_descriptors_by_size[lower_bound:upper_bound]
        ]

    def _needs_to_sync(
        self,
        client_file_descriptor: _FileDescriptor,
        client_previous_mtime_by_path: Mapping[str, float],
    ) -> bool:
        """Return True iff the given file needs to be synced."""
        return (
            # The server doesn't have a copy.
            not (absolute_path := self.dir / client_file_descriptor.path).exists()
            # The file has changed size.
            or (stat := absolute_path.stat()).st_size != client_file_descriptor.filesize
            # The client's version has been modified after the last sync.
            or client_file_descriptor.path not in client_previous_mtime_by_path
            or client_previous_mtime_by_path[client_file_descriptor.path]
            < client_file_descriptor.mtime
        )

    def _clean_up_directory(self, client_dir_descriptor: _DirectoryDescriptor) -> None:
        """Removes files and subdirectories which don't exist in the client."""
        client_paths = set(
            pathlib.Path(file_descriptor.path)
            for file_descriptor in client_dir_descriptor.file_descriptors
        ) | set(map(pathlib.Path, client_dir_descriptor.sub_directories))

        # Topological sort so that directories are emptied before removal.
        for path in sorted(self.dir.rglob("*"), reverse=True):
            if path.relative_to(self.dir) not in client_paths:
                if path.is_file():
                    logging.info(f"Removing file: '{path}'.")
                    path.unlink()
                else:
                    logging.info(f"Removing directory: '{path}'.")
                    path.rmdir()


async def serve(dir: pathlib.Path, fuzziness: int, sync_wait_sec: float) -> None:
    async with grpc.aio.insecure_channel(client_addr) as channel:
        server = SyncServer(
            pathlib.Path(args.dir),
            args.fuzziness,
            arlosync_pb2_grpc.SyncClientStub(channel),
        )
        while True:
            await asyncio.sleep(sync_wait_sec)
            try:
                await server.sync_directory()
            except Exception as e:
                logging.error(e)


if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    client_addr = f"localhost:{args.port}"

    asyncio.get_event_loop().run_until_complete(
        serve(pathlib.Path(args.dir), args.fuzziness, args.sync_wait_sec)
    )
