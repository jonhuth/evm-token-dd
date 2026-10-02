#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from evm import (  # noqa: E402
    AddressError,
    PinError,
    is_placeholder_pin_value,
    pin_matches_header,
    to_checksum_address,
    uniswap_v4_pool_id,
)
from keccak import keccak256  # noqa: E402
from skill_home import skill_home  # noqa: E402


class KeccakTests(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertEqual(
            keccak256(b"").hex(),
            "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470",
        )

    def test_abc(self) -> None:
        self.assertEqual(
            keccak256(b"abc").hex(),
            "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45",
        )


class AddressTests(unittest.TestCase):
    def test_eip55_vectors(self) -> None:
        vectors = (
            "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed",
            "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359",
            "0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB",
            "0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb",
        )
        for addr in vectors:
            self.assertEqual(to_checksum_address(addr.lower()), addr)

    def test_rejects_malformed(self) -> None:
        with self.assertRaises(AddressError):
            to_checksum_address("0x123")
        with self.assertRaises(AddressError):
            to_checksum_address("1111111111111111111111111111111111111111")


class PinTests(unittest.TestCase):
    def test_placeholders(self) -> None:
        for value in ("latest", "pending", "0x0", 0, None, "TODO", "0x" + "0" * 64):
            self.assertTrue(is_placeholder_pin_value(value), value)

    def test_header_mismatch(self) -> None:
        pin = {
            "block_number": 10,
            "block_hash": "0x" + "aa" * 32,
            "timestamp_utc": "2024-03-09T16:00:00Z",
            "header": {
                "number": 11,
                "hash": "0x" + "aa" * 32,
                "timestamp": 1710000000,
            },
        }
        with self.assertRaises(PinError):
            pin_matches_header(pin)

    def test_header_match(self) -> None:
        pin = {
            "block_number": 18000000,
            "block_hash": "0x" + "aa" * 32,
            "timestamp_utc": "2024-03-09T16:00:00Z",
            "header": {
                "number": 18000000,
                "hash": "0x" + "AA" * 32,
                "timestamp": 1710000000,
            },
        }
        pin_matches_header(pin)


class PoolIdTests(unittest.TestCase):
    def test_order_required(self) -> None:
        with self.assertRaises(ValueError):
            uniswap_v4_pool_id(
                "0x0000000000000000000000000000000000000002",
                "0x0000000000000000000000000000000000000001",
                3000,
                60,
                "0x0000000000000000000000000000000000000000",
            )

    def test_hook_changes_id(self) -> None:
        args = {
            "currency0": "0x0000000000000000000000000000000000000000",
            "currency1": "0x0000000000000000000000000000000000000001",
            "fee": 3000,
            "tick_spacing": 60,
        }
        none = uniswap_v4_pool_id(**args, hooks="0x0000000000000000000000000000000000000000")
        hooked = uniswap_v4_pool_id(**args, hooks="0x0000000000000000000000000000000000000002")
        self.assertNotEqual(none, hooked)
        self.assertTrue(none.startswith("0x"))
        self.assertEqual(len(none), 66)


class SkillHomeTests(unittest.TestCase):
    def test_package_relative(self) -> None:
        home = skill_home()
        self.assertTrue((home / "SKILL.md").is_file())
        # Package root is the directory holding SKILL.md, whatever the checkout is named.
        self.assertEqual(home, Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    unittest.main()
