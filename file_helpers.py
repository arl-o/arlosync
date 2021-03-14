import math
import pathlib

from arlosync.protos import arlosync_pb2


def build_directory_descriptor(dir: pathlib.Path):
    """Builds a sorted (consistent) view of directory metadata."""
    directory_descriptor = arlosync_pb2.DirectoryDescriptor()
    for path in sorted(dir.rglob("*")):
        if path.is_file():
            stat = path.stat()
            directory_descriptor.file_descriptors.append(
                arlosync_pb2.FileDescriptor(
                    path=str(path.relative_to(dir)),
                    filesize=stat.st_size,
                    mtime=stat.st_mtime,
                )
            )
        else:
            directory_descriptor.sub_directories.append(str(path.relative_to(dir)))
    return directory_descriptor


def get_optimal_chunk_size(
    file_size_bytes: int,
    max_chunk_size: int = 10 ** 6,
    hash_size_bytes: int = 32,
    checksum_size_bytes: int = 32,
    num_expected_untokenized_chunks: float = 1,
) -> int:
    """Approximately minimizes the number of bidirectional transferred bytes.

    Assumes no overhead, and that `num_expected_untokenized_chunks` are not
    tokenized (i.e. different between client and server). Achieves O(sqrt(N))
    transferred bytes for small `num_expected_untokenized_chunks`, where N is
    the size of the file.

    Returns:
        Approximately optimal chunk size.
        min: `hash_size_bytes` * 2
        max: `max_chunk_size`
    """
    approx_optimal = math.sqrt(
        (1 / num_expected_untokenized_chunks)
        * (2 * hash_size_bytes + checksum_size_bytes)
        * file_size_bytes
    )
    return round(min(max_chunk_size, max(hash_size_bytes * 2, approx_optimal)))
