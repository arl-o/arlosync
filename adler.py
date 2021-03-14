# Simple implementation of adler-32 rolling algorithm, as per:
# https://en.wikipedia.org/wiki/Adler-32

from typing import Iterable

MOD_ADLER = 65521

class adler32:
    def __init__(self, data: bytes):
        self.block_size = len(data)
        self.a, self.b = 1, 0
        for char in data:
            self.a = (self.a + char) % MOD_ADLER
            self.b = (self.b + self.a) % MOD_ADLER

    def update(self, added: int, removed: int):
        self.a = (self.a + added - removed) % MOD_ADLER
        self.b = (self.b - (self.block_size * removed) + self.a - 1) % MOD_ADLER

    def digest(self) -> int:
        return (self.b << 16) | self.a
