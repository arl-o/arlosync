import unittest
from zlib import adler32 as builtin_adler32

from arlosync.adler import adler32


class TestAdlerChecksum(unittest.TestCase):
    def test_matches_initalized(self):
        in_bytes = b"Why don't ants get sick? They have ant-y bodies."
        self.assertEqual(builtin_adler32(in_bytes), adler32(in_bytes).digest())

    def test_matches_with_update(self):
        in_bytes = b"abcdefYZ"
        rolling_checksum = adler32(b"ABabcdef")
        self.assertNotEqual(builtin_adler32(in_bytes), rolling_checksum.digest())
        rolling_checksum.update(ord(b"Y"), ord(b"A"))
        rolling_checksum.update(ord(b"Z"), ord(b"B"))
        self.assertEqual(builtin_adler32(in_bytes), rolling_checksum.digest())
