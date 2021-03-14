import unittest

from arlosync import file_helpers


def _approx_network_cost_bytes(
    hash_size_bytes: float,
    checksum_size_bytes: int,
    file_size_bytes: float,
    num_untokenized_chunks: float,
    chunk_size_bytes: float,
) -> float:
    """Cost (in bytes) of bidirectional network transfer, assuming no overhead."""
    num_chunks = file_size_bytes / chunk_size_bytes
    return (
        # Sent to client
        num_chunks * (hash_size_bytes + checksum_size_bytes)
        # Returned from client
        + (num_chunks - num_untokenized_chunks) * hash_size_bytes
        + (num_untokenized_chunks * chunk_size_bytes)
    )


class TestChunkLogic(unittest.TestCase):
    def test_within_bounds_of_optimal(self):
        within_percent_bound_of_optimal = 0.0001  # 0.01%
        file_size_bytes = 1e6
        for num_untokenized_chunks in (1, 4, 8):
            supposedly_optimal = file_helpers.get_optimal_chunk_size(
                file_size_bytes,
                hash_size_bytes=32,  # blake2s
                checksum_size_bytes=32,  # adler32
                num_expected_untokenized_chunks=num_untokenized_chunks,
            )

            self.assertTrue(
                _approx_network_cost_bytes(
                    32,
                    32,
                    file_size_bytes,
                    num_untokenized_chunks,
                    supposedly_optimal * (1 - within_percent_bound_of_optimal),
                )
                > _approx_network_cost_bytes(
                    32,
                    32,
                    file_size_bytes,
                    num_untokenized_chunks,
                    supposedly_optimal,
                )
                < _approx_network_cost_bytes(
                    32,
                    32,
                    file_size_bytes,
                    num_untokenized_chunks,
                    supposedly_optimal * (1 + within_percent_bound_of_optimal),
                ),
            )

        self.assertTrue(
            "Who knows how to use simple derivatives for optimization problems? This gal."
        )
