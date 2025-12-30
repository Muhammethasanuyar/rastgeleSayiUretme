# splitmix64_rng.py
# SplitMix64: hızlı, deterministik 64-bit PRNG (kriptografik amaçlar için uygun değildir)

from __future__ import annotations
from dataclasses import dataclass

MASK64 = (1 << 64) - 1

@dataclass
class SplitMix64:
    state: int

    def next_u64(self) -> int:
        """Bir sonraki 64-bit rastgele sayı (0..2^64-1)."""
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        z = (z ^ (z >> 31)) & MASK64
        return z

    def randbelow(self, n: int) -> int:
        """0..n-1 aralığında sayı (basit mod alma)."""
        if n <= 0:
            raise ValueError("n > 0 olmalı")
        return self.next_u64() % n

    def random(self) -> float:
        """[0,1) aralığında float üretir (53-bit hassasiyet)."""
        return (self.next_u64() >> 11) / float(1 << 53)


if __name__ == "__main__":
    seed = 20251230
    rng = SplitMix64(seed)

    print(f"Seed = {seed}")
    print("İlk 10 çıktı (hex ve decimal):")
    for i in range(10):
        x = rng.next_u64()
        print(f"{i+1:2d}) {x:#018x}  ->  {x}")
