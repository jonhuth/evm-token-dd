#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_report import SELF_TEST_CASES, validate  # noqa: E402


def load_fixture(name: str) -> tuple[dict, dict]:
    payload = json.loads((ROOT / "tests" / "fixtures" / name).read_text())
    return payload["manifest"], payload["report"]


class FixtureTests(unittest.TestCase):
    def test_self_test_cases(self) -> None:
        for name, expected in SELF_TEST_CASES:
            manifest, report = load_fixture(name)
            codes = {issue.code for issue in validate(manifest, report)}
            if expected:
                self.assertTrue(
                    codes.intersection(expected),
                    f"{name}: expected one of {expected}, got {sorted(codes)}",
                )
            else:
                self.assertEqual(codes, set(), f"{name}: unexpected {sorted(codes)}")

    def test_placeholder_pin_rejected(self) -> None:
        manifest, report = load_fixture("valid_broad.json")
        manifest = deepcopy(manifest)
        manifest["pin"]["block_number"] = "latest"
        codes = {issue.code for issue in validate(manifest, report)}
        self.assertIn("PIN_PLACEHOLDER", codes)

    def test_malformed_address_rejected(self) -> None:
        manifest, report = load_fixture("valid_broad.json")
        manifest = deepcopy(manifest)
        manifest["requested"]["address"] = "0x123"
        codes = {issue.code for issue in validate(manifest, report)}
        self.assertTrue(codes.intersection({"TARGET_MISSING", "ADDRESS_MALFORMED"}))

    def test_unresolved_metadata_cannot_be_invented(self) -> None:
        manifest, report = load_fixture("valid_broad.json")
        manifest = deepcopy(manifest)
        report = deepcopy(report)
        manifest["observed"]["name"] = None
        manifest["observed"]["metadata_status"] = "resolved"
        codes = {issue.code for issue in validate(manifest, report)}
        self.assertIn("METADATA_INCONSISTENT", codes)


if __name__ == "__main__":
    unittest.main()
