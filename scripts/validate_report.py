#!/usr/bin/env python3
"""Validate a target-integrity manifest against a broad diligence report.

Passing means internal consistency only. It does not prove RPC honesty,
discovery completeness, or protocol safety.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Allow `python scripts/validate_report.py` from any cwd.
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from evm import (  # noqa: E402
    PinError,
    is_address,
    parse_chain_id,
    pin_matches_header,
    target_key,
    to_checksum_address,
)
from skill_home import fixtures_dir, skill_home  # noqa: E402

SKILL_NAME = "evm-token-due-diligence"
RATING_KEYS = (
    "token_controls",
    "canonical_lp_principal_custody",
    "side_pool_removal_risk",
    "sellability_and_exit_depth",
    "current_concentration",
    "historical_launch_integrity",
    "admin_treasury_and_reward_custody",
    "reward_accounting_and_liveness",
    "utility_and_redemption_rights",
    "external_dependencies",
    "development_and_disclosure",
)
PASS_LIKE = {"pass", "ok", "cleared", "safe"}
UNKNOWN_LIKE = {"unknown", "skipped", "unresolved", "not_checked", "pending"}
CHECK_STATUSES = {
    "pass",
    "fail",
    "unknown",
    "skipped",
    "not-applicable",
    "not_applicable",
}
EVIDENCE_FIELDS = (
    "id",
    "proposition",
    "chain_id",
    "address",
    "pin_or_tx",
    "artifact_or_query",
    "decoding_basis",
    "evidence_type",
    "confidence",
    "coverage",
    "stale_if",
)
SCOPE_FIELDS = ("address", "chain_id", "role", "provenance", "runtime_status")
SAFE_VERDICT_RE = ("this token is safe", "unconditionally safe", "safe to buy")


class Issue:
    def __init__(self, code: str, message: str, path: str) -> None:
        self.code = code
        self.message = message
        self.path = path

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _identity(obj: dict[str, Any], label: str) -> tuple[int | None, str | None, str | None]:
    block = obj.get("identity") if isinstance(obj.get("identity"), dict) else obj
    requested = obj.get("requested") if isinstance(obj.get("requested"), dict) else {}
    observed = obj.get("observed") if isinstance(obj.get("observed"), dict) else {}
    reported = obj.get("reported") if isinstance(obj.get("reported"), dict) else {}
    chain = block.get(
        "chain_id", requested.get("chain_id", observed.get("chain_id", reported.get("chain_id")))
    )
    address = block.get(
        "address", requested.get("address", observed.get("address", reported.get("address")))
    )
    inv = block.get("investigation_id") or obj.get("investigation_id")
    try:
        chain_id = parse_chain_id(chain) if chain is not None else None
    except ValueError:
        chain_id = None
    addr = None
    if isinstance(address, str) and is_address(address):
        addr = to_checksum_address(address)
    return chain_id, addr, inv if isinstance(inv, str) else None


def _chain_addr(
    obj: dict[str, Any] | None, fallback: dict[str, Any] | None = None
) -> tuple[int | None, str | None]:
    data = obj if isinstance(obj, dict) else {}
    fb = fallback if isinstance(fallback, dict) else {}
    chain = data.get("chain_id", fb.get("chain_id"))
    address = data.get("address", fb.get("address"))
    chain_id = None
    if chain is not None:
        try:
            chain_id = parse_chain_id(chain)
        except ValueError:
            chain_id = None
    addr = None
    if isinstance(address, str) and is_address(address):
        addr = to_checksum_address(address)
    return chain_id, addr


def validate(manifest: dict[str, Any], report: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    def err(code: str, message: str, path: str) -> None:
        issues.append(Issue(code, message, path))

    if not isinstance(manifest, dict):
        return [Issue("MANIFEST_INVALID", "manifest must be an object", "$")]
    if not isinstance(report, dict):
        return [Issue("REPORT_INVALID", "report must be an object", "$")]

    for label, obj in (("manifest", manifest), ("report", report)):
        skill = obj.get("skill")
        if skill not in (None, SKILL_NAME):
            err(
                "SKILL_MISMATCH",
                f"{label} skill is {skill!r}, expected {SKILL_NAME!r}",
                f"{label}.skill",
            )

    req_c, req_a = _chain_addr(
        manifest.get("requested") if isinstance(manifest.get("requested"), dict) else None
    )
    obs_c, obs_a = _chain_addr(
        manifest.get("observed") if isinstance(manifest.get("observed"), dict) else None,
        manifest.get("requested") if isinstance(manifest.get("requested"), dict) else None,
    )
    rep_c, rep_a = _chain_addr(
        report.get("reported") if isinstance(report.get("reported"), dict) else None,
        report.get("requested") if isinstance(report.get("requested"), dict) else None,
    )
    report_req_c, report_req_a = _chain_addr(
        report.get("requested") if isinstance(report.get("requested"), dict) else None
    )

    if req_c is None or req_a is None:
        err(
            "TARGET_MISSING",
            "manifest.requested must include a valid chain_id and address",
            "manifest.requested",
        )
        return issues

    for label, chain, addr in (
        ("manifest.observed", obs_c, obs_a),
        ("report.requested", report_req_c, report_req_a if report_req_a is not None else req_a),
        ("report.reported", rep_c, rep_a),
    ):
        if chain is None or addr is None:
            err("TARGET_MISSING", f"{label} must include a valid chain_id and address", label)
            continue
        if chain != req_c or addr != req_a:
            same_symbol = False
            req_meta = (
                manifest.get("requested") if isinstance(manifest.get("requested"), dict) else {}
            )
            obs_meta = (
                manifest.get("observed") if isinstance(manifest.get("observed"), dict) else {}
            )
            rep_meta = report.get("reported") if isinstance(report.get("reported"), dict) else {}
            symbols = {
                str(req_meta.get("symbol") or "").strip().upper(),
                str(obs_meta.get("symbol") or "").strip().upper(),
                str(rep_meta.get("symbol") or "").strip().upper(),
            }
            symbols.discard("")
            if chain != req_c and len(symbols) == 1:
                same_symbol = True
            if same_symbol:
                err(
                    "SAME_SYMBOL_SUBSTITUTION",
                    f"{label} is chain {chain} {addr} with the same symbol as requested "
                    f"chain {req_c} {req_a}. Never substitute a same-symbol token.",
                    label,
                )
            elif addr != req_a:
                err(
                    "TARGET_MISMATCH",
                    f"{label} address {addr} does not match requested {req_a}",
                    label,
                )
            else:
                err(
                    "CHAIN_MISMATCH",
                    f"{label} chain {chain} does not match requested chain {req_c}",
                    label,
                )

    man_id = None
    if isinstance(manifest.get("identity"), dict):
        man_id = manifest["identity"].get("investigation_id")
    man_id = man_id or manifest.get("investigation_id")
    rep_id = None
    if isinstance(report.get("identity"), dict):
        rep_id = report["identity"].get("investigation_id")
    rep_id = rep_id or report.get("investigation_id") or report.get("manifest_id")
    if not man_id or not isinstance(man_id, str):
        err(
            "IDENTITY_MISSING",
            "manifest identity.investigation_id is required",
            "manifest.identity.investigation_id",
        )
    if not rep_id or not isinstance(rep_id, str):
        err(
            "IDENTITY_MISSING",
            "report identity.investigation_id is required",
            "report.identity.investigation_id",
        )
    if man_id and rep_id and man_id != rep_id:
        err(
            "IDENTITY_MISMATCH",
            f"report investigation_id {rep_id!r} does not match manifest {man_id!r}",
            "report.identity.investigation_id",
        )

    expected_key = target_key(req_c, req_a)
    for label, obj in (("manifest", manifest), ("report", report)):
        ident = obj.get("identity") if isinstance(obj.get("identity"), dict) else {}
        key = ident.get("target_key") or obj.get("target_key")
        if key and key != expected_key:
            err(
                "IDENTITY_MISMATCH",
                f"{label} target_key {key!r} != {expected_key!r}",
                f"{label}.identity.target_key",
            )

    observed = manifest.get("observed") if isinstance(manifest.get("observed"), dict) else {}
    reported = report.get("reported") if isinstance(report.get("reported"), dict) else {}
    meta_status = str(observed.get("metadata_status") or "").strip().lower()
    unresolved_fields = observed.get("unresolved_metadata_fields") or []
    if not isinstance(unresolved_fields, list):
        unresolved_fields = []
    for field in ("name", "symbol", "decimals"):
        value = observed.get(field)
        if value in (None, "", "unresolved", "unknown"):
            if meta_status not in {"unresolved", "nonstandard"}:
                err(
                    "METADATA_INCONSISTENT",
                    f"observed.{field} is unresolved but metadata_status is {meta_status!r}",
                    f"manifest.observed.{field}",
                )
            if field not in unresolved_fields:
                err(
                    "METADATA_INCONSISTENT",
                    f"observed.{field} is unresolved but missing from unresolved_metadata_fields",
                    "manifest.observed.unresolved_metadata_fields",
                )
            if reported.get(field) not in (None, "", "unresolved", "unknown", value):
                err(
                    "METADATA_INCONSISTENT",
                    f"report invented {field}={reported.get(field)!r} while observed is unresolved",
                    f"report.reported.{field}",
                )
        elif reported.get(field) not in (None, value):
            # decimals may be int vs string
            if str(reported.get(field)) != str(value):
                err(
                    "METADATA_INCONSISTENT",
                    f"reported.{field}={reported.get(field)!r} != observed.{field}={value!r}",
                    f"report.reported.{field}",
                )

    pin = manifest.get("pin") if isinstance(manifest.get("pin"), dict) else None
    if pin is None:
        err("PIN_MISSING", "manifest.pin is required", "manifest.pin")
    else:
        try:
            pin_chain = parse_chain_id(pin.get("chain_id", req_c))
            if pin_chain != req_c:
                err(
                    "CHAIN_MISMATCH",
                    f"pin chain {pin_chain} != requested {req_c}",
                    "manifest.pin.chain_id",
                )
            pin_matches_header(pin)
        except (PinError, ValueError) as exc:
            message = str(exc)
            code = "PIN_PLACEHOLDER" if "placeholder" in message.lower() else "PIN_MISMATCH"
            err(code, message, "manifest.pin")

    additional = manifest.get("additional_pins") or []
    extra_pins: dict[int, dict[str, Any]] = {}
    if additional and not isinstance(additional, list):
        err("PIN_MISMATCH", "additional_pins must be an array", "manifest.additional_pins")
        additional = []
    for i, extra in enumerate(additional):
        if not isinstance(extra, dict):
            err(
                "PIN_MISMATCH", "additional pin must be an object", f"manifest.additional_pins[{i}]"
            )
            continue
        try:
            cid = parse_chain_id(extra.get("chain_id"))
            pin_matches_header(extra)
            extra_pins[cid] = extra
        except (PinError, ValueError) as exc:
            message = str(exc)
            code = "PIN_PLACEHOLDER" if "placeholder" in message.lower() else "PIN_MISMATCH"
            err(code, message, f"manifest.additional_pins[{i}]")

    pinned_chains = {req_c, *extra_pins}

    for i, scope in enumerate(manifest.get("scope_addresses") or []):
        path = f"manifest.scope_addresses[{i}]"
        if not isinstance(scope, dict):
            err("SCOPE_INCOMPLETE", "scope address must be an object", path)
            continue
        for field in SCOPE_FIELDS:
            if not scope.get(field):
                err("SCOPE_INCOMPLETE", f"scope address missing {field}", f"{path}.{field}")
        addr = scope.get("address")
        if addr is not None and not is_address(addr):
            err("ADDRESS_MALFORMED", f"malformed scope address: {addr!r}", f"{path}.address")
        try:
            cid = parse_chain_id(scope.get("chain_id"))
        except ValueError:
            err("SCOPE_INCOMPLETE", "scope address has invalid chain_id", f"{path}.chain_id")
            continue
        if cid not in pinned_chains:
            err(
                "SCOPE_CHAIN_UNPINNED",
                f"scope address on chain {cid} has no pin for that chain",
                path,
            )

    for i, finding in enumerate(report.get("findings") or []):
        path = f"report.findings[{i}]"
        if not isinstance(finding, dict):
            err("EVIDENCE_MISSING", "finding must be an object", path)
            continue
        for field in EVIDENCE_FIELDS:
            if finding.get(field) in (None, ""):
                err("EVIDENCE_MISSING", f"finding missing {field}", f"{path}.{field}")
        if finding.get("address") and not is_address(finding.get("address")):
            err(
                "ADDRESS_MALFORMED",
                f"malformed finding address: {finding.get('address')!r}",
                f"{path}.address",
            )
        if finding.get("chain_id") is not None:
            try:
                parse_chain_id(finding.get("chain_id"))
            except ValueError:
                err("CHAIN_MISMATCH", "finding has invalid chain_id", f"{path}.chain_id")
        conf = str(finding.get("confidence") or "").lower()
        if conf == "unknown" and str(finding.get("status") or "").lower() in PASS_LIKE:
            err(
                "UNKNOWN_AS_PASS",
                f"finding {finding.get('id')!r} is unknown but marked pass",
                path,
            )

    checks = report.get("checks") or []
    check_by_id: dict[str, dict[str, Any]] = {}
    if checks and not isinstance(checks, list):
        err("EVIDENCE_MISSING", "report.checks must be an array", "report.checks")
        checks = []
    for i, check in enumerate(checks):
        path = f"report.checks[{i}]"
        if not isinstance(check, dict):
            err("EVIDENCE_MISSING", "check must be an object", path)
            continue
        cid = check.get("id")
        status = str(check.get("status") or "").strip().lower()
        if not cid:
            err("EVIDENCE_MISSING", "check missing id", f"{path}.id")
            continue
        check_by_id[str(cid)] = check
        if status not in CHECK_STATUSES:
            err(
                "EVIDENCE_MISSING", f"check {cid!r} has invalid status {status!r}", f"{path}.status"
            )
        if status in UNKNOWN_LIKE and (
            check.get("as_pass") is True
            or str(check.get("treated_as") or "").lower() in PASS_LIKE
            or str(check.get("rating") or "").lower() in PASS_LIKE
        ):
            err(
                "UNKNOWN_AS_PASS",
                f"check {cid!r} is {status} but presented as a pass",
                path,
            )

    ratings = report.get("ratings") if isinstance(report.get("ratings"), dict) else {}
    for key in RATING_KEYS:
        rating = ratings.get(key)
        if not isinstance(rating, dict):
            continue
        status = str(rating.get("status") or "").strip().lower()
        supporting = rating.get("check_ids") or rating.get("supporting_check_ids") or []
        if not isinstance(supporting, list):
            supporting = []
        unknown_ids = []
        for check_id in supporting:
            check = check_by_id.get(str(check_id))
            if not check:
                continue
            if str(check.get("status") or "").lower() in UNKNOWN_LIKE:
                unknown_ids.append(str(check_id))
        if status in PASS_LIKE and unknown_ids:
            err(
                "UNKNOWN_AS_PASS",
                f"rating {key} is pass but depends on unknown/skipped checks {unknown_ids}",
                f"report.ratings.{key}",
            )
        if status in PASS_LIKE and str(rating.get("coverage") or "").lower() in UNKNOWN_LIKE:
            err(
                "UNKNOWN_AS_PASS",
                f"rating {key} is pass but coverage is unknown",
                f"report.ratings.{key}",
            )

    safety = manifest.get("safety") if isinstance(manifest.get("safety"), dict) else {}
    report_safety = report.get("safety") if isinstance(report.get("safety"), dict) else safety
    for payload, label in ((safety, "manifest.safety"), (report_safety, "report.safety")):
        if payload.get("no_real_signing") is not True:
            err("SAFETY_VIOLATION", "no_real_signing must be true", f"{label}.no_real_signing")
        if payload.get("no_broadcast") is not True:
            err("SAFETY_VIOLATION", "no_broadcast must be true", f"{label}.no_broadcast")
        if payload.get("fork_used") is True:
            restrictions = payload.get("fork_restrictions")
            if not restrictions:
                err(
                    "SAFETY_VIOLATION",
                    "fork_used requires fork_restrictions (disposable local fork, synthetic accounts, counterfactual label)",
                    f"{label}.fork_restrictions",
                )

    verdict = report.get("verdict") if isinstance(report.get("verdict"), dict) else {}
    answer = str(verdict.get("answer") or "").strip().lower()
    go = str(verdict.get("go_nogo") or "").strip().upper()
    if verdict.get("unconditional_safe") is True or answer in {"safe", "this token is safe"}:
        err(
            "UNCONDITIONAL_SAFE",
            "unconditional 'safe' verdicts are forbidden",
            "report.verdict",
        )
    if go == "GO" and verdict.get("conditional") is not True:
        err(
            "UNCONDITIONAL_SAFE",
            "GO verdicts must be marked conditional",
            "report.verdict.conditional",
        )
    for phrase in SAFE_VERDICT_RE:
        if phrase in answer:
            err(
                "UNCONDITIONAL_SAFE",
                "verdict language implies unconditional safety",
                "report.verdict.answer",
            )

    findings = report.get("findings") or []
    if go in {"GO", "CONDITIONAL"} and not findings:
        err(
            "EVIDENCE_MISSING",
            "GO/CONDITIONAL verdicts require at least one evidence-backed finding",
            "report.findings",
        )

    return issues


SELF_TEST_CASES = (
    ("valid_broad.json", ()),
    ("same_symbol_other_chain.json", ("SAME_SYMBOL_SUBSTITUTION",)),
    ("wrong_target.json", ("TARGET_MISMATCH",)),
    ("fake_block_pin.json", ("PIN_MISMATCH", "PIN_PLACEHOLDER")),
    ("unknown_as_pass.json", ("UNKNOWN_AS_PASS",)),
)


def _pair_from_fixture(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if "manifest" in payload and "report" in payload:
        return payload["manifest"], payload["report"]
    raise ValueError("fixture must contain manifest and report objects")


def run_self_test() -> int:
    fixtures = fixtures_dir()
    failed = 0
    for name, expected_codes in SELF_TEST_CASES:
        path = fixtures / name
        payload = _load_json(path)
        manifest, report = _pair_from_fixture(payload)
        codes = {issue.code for issue in validate(manifest, report)}
        expected = set(expected_codes)
        if expected:
            if codes.isdisjoint(expected):
                failed += 1
                print(f"FAIL {name}: expected one of {sorted(expected)}, got {sorted(codes)}")
            else:
                print(f"PASS {name}: rejected ({', '.join(sorted(codes & expected))})")
        else:
            if codes:
                failed += 1
                print(f"FAIL {name}: expected pass, got {sorted(codes)}")
            else:
                print(f"PASS {name}: internally consistent")
    if failed:
        print(f"self-test: {failed} failed")
        return 1
    print("self-test: all cases passed")
    print(
        "Note: passing validates internal consistency, not RPC honesty, "
        "discovery completeness, or protocol safety."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate target-integrity manifest vs broad report. "
            "Passing validates internal consistency, not RPC honesty, "
            "discovery completeness, or protocol safety."
        )
    )
    parser.add_argument("--manifest", type=Path, help="target-integrity JSON")
    parser.add_argument("--report", type=Path, help="broad report JSON")
    parser.add_argument("--self-test", action="store_true", help="run synthetic rejection fixtures")
    parser.add_argument("--print-home", action="store_true", help="print resolved skill home")
    args = parser.parse_args(argv)

    if args.print_home:
        print(skill_home())
        return 0
    if args.self_test:
        return run_self_test()
    if not args.manifest or not args.report:
        parser.error("provide --manifest and --report, or --self-test")

    issues = validate(_load_json(args.manifest), _load_json(args.report))
    if not issues:
        print("PASS: manifest and report are internally consistent")
        print(
            "Passing validates internal consistency, not RPC honesty, "
            "discovery completeness, or protocol safety."
        )
        return 0
    print("FAIL: integrity checks failed")
    for issue in issues:
        print(f"  [{issue.code}] {issue.path}: {issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
