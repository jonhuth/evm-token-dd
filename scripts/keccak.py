"""Keccak-256 (Ethereum / pre-NIST). Stdlib only.

NIST SHA3-256 in hashlib is a different hash. Do not substitute it.
"""

from __future__ import annotations

_RC = (
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008,
)

_ROT = (
    (0, 36, 3, 41, 18),
    (1, 44, 10, 45, 2),
    (62, 6, 43, 15, 61),
    (28, 55, 25, 21, 56),
    (27, 20, 39, 8, 14),
)

_MASK = (1 << 64) - 1


def _rotl(x: int, n: int) -> int:
    return ((x << n) | (x >> (64 - n))) & _MASK


def _keccak_f(st: list[int]) -> None:
    for rc in _RC:
        c = [st[x] ^ st[x + 5] ^ st[x + 10] ^ st[x + 15] ^ st[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rotl(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                st[x + 5 * y] ^= d[x]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rotl(st[x + 5 * y], _ROT[x][y])
        for x in range(5):
            for y in range(5):
                st[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y])
                st[x + 5 * y] &= _MASK
        st[0] ^= rc


def keccak256(data: bytes) -> bytes:
    """Return the 32-byte Keccak-256 digest."""
    rate = 136
    st = [0] * 25
    offset = 0
    length = len(data)
    while offset + rate <= length:
        block = data[offset : offset + rate]
        for i in range(rate // 8):
            st[i] ^= int.from_bytes(block[i * 8 : (i + 1) * 8], "little")
        _keccak_f(st)
        offset += rate
    block = bytearray(data[offset:])
    block.append(0x01)
    block.extend(b"\x00" * (rate - len(block)))
    block[-1] |= 0x80
    for i in range(rate // 8):
        st[i] ^= int.from_bytes(block[i * 8 : (i + 1) * 8], "little")
    _keccak_f(st)
    out = bytearray()
    for i in range(4):
        out.extend(st[i].to_bytes(8, "little"))
    return bytes(out)
