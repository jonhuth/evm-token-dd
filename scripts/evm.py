"""Address, pin, and Uniswap v4 PoolId helpers. No RPC, no keys."""

from __future__ import annotations

import re
from typing import Any

try:
    from datetime import UTC, datetime
except ImportError:
    from datetime import datetime, timezone
    UTC = timezone.utc

from keccak import keccak256

ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
BYTES32_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")
PLACEHOLDER_PINS = {
    "",
    "0",
    "latest",
    "pending",
    "safe",
    "finalized",
    "todo",
    "unknown",
    "tbd",
    "null",
    "none",
    "placeholder",
}


class AddressError(ValueError):
    pass


class PinError(ValueError):
    pass


def is_address(value: Any) -> bool:
    return isinstance(value, str) and bool(ADDRESS_RE.fullmatch(value.strip()))


def normalize_address(value: str) -> str:
    if not is_address(value):
        raise AddressError(f"malformed address: {value!r}")
    return value.strip().lower()


def to_checksum_address(value: str) -> str:
    raw = normalize_address(value)[2:]
    digest = keccak256(raw.encode("ascii")).hex()
    out = ["0x"]
    for char, nibble in zip(raw, digest):
        out.append(char.upper() if int(nibble, 16) >= 8 else char)
    return "".join(out)


def addresses_equal(left: str, right: str) -> bool:
    return normalize_address(left) == normalize_address(right)


def parse_chain_id(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        raise ValueError(f"invalid chain id: {value!r}")
    if isinstance(value, int):
        chain_id = value
    elif isinstance(value, str):
        text = value.strip().lower()
        chain_id = int(text, 16) if text.startswith("0x") else int(text, 10)
    else:
        raise ValueError(f"invalid chain id: {value!r}")
    if chain_id < 0:
        raise ValueError(f"invalid chain id: {value!r}")
    return chain_id


def parse_block_number(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        raise PinError(f"invalid block number: {value!r}")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str):
        text = value.strip().lower()
        if text in PLACEHOLDER_PINS:
            raise PinError(f"placeholder block number: {value!r}")
        number = int(text, 16) if text.startswith("0x") else int(text, 10)
    else:
        raise PinError(f"invalid block number: {value!r}")
    if number < 0:
        raise PinError(f"invalid block number: {value!r}")
    return number


def is_placeholder_pin_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in PLACEHOLDER_PINS:
        return True
    if isinstance(value, str) and value.strip().lower() in {"0x", "0x0"}:
        return True
    if isinstance(value, str) and re.fullmatch(r"0x0+", value.strip().lower()):
        return True
    if value == 0:
        return True
    return False


def require_block_hash(value: Any) -> str:
    if not isinstance(value, str) or not BYTES32_RE.fullmatch(value.strip()):
        raise PinError(f"malformed block hash: {value!r}")
    digest = value.strip().lower()
    if digest == "0x" + ("0" * 64):
        raise PinError("placeholder block hash (all zero)")
    return digest


def parse_unix_timestamp(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        raise PinError(f"invalid timestamp: {value!r}")
    if isinstance(value, int):
        if value <= 0:
            raise PinError(f"placeholder timestamp: {value!r}")
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.lower() in PLACEHOLDER_PINS:
            raise PinError(f"placeholder timestamp: {value!r}")
        if re.fullmatch(r"\d+", text):
            unix = int(text, 10)
            if unix <= 0:
                raise PinError(f"placeholder timestamp: {value!r}")
            return unix
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        unix = int(parsed.timestamp())
        if unix <= 0:
            raise PinError(f"placeholder timestamp: {value!r}")
        return unix
    raise PinError(f"invalid timestamp: {value!r}")


def pin_matches_header(pin: dict[str, Any], header: dict[str, Any] | None = None) -> None:
    """Raise PinError if the pin is a placeholder or disagrees with its header."""
    header = header if header is not None else pin.get("header")
    if not isinstance(pin, dict):
        raise PinError("pin must be an object")
    if not isinstance(header, dict):
        raise PinError("pin header missing")
    number = parse_block_number(pin.get("block_number"))
    block_hash = require_block_hash(pin.get("block_hash"))
    ts = parse_unix_timestamp(pin.get("timestamp_utc", pin.get("timestamp")))
    header_number = parse_block_number(header.get("number", header.get("block_number")))
    header_hash = require_block_hash(header.get("hash", header.get("block_hash")))
    header_ts = parse_unix_timestamp(header.get("timestamp", header.get("timestamp_utc")))
    if number != header_number:
        raise PinError(f"block number {number} != header.number {header_number}")
    if block_hash != header_hash:
        raise PinError("block hash does not match captured header")
    if ts != header_ts:
        raise PinError(f"timestamp {ts} != header.timestamp {header_ts}")
    if is_placeholder_pin_value(pin.get("block_number")):
        raise PinError("placeholder block number")


def _pad32(value: bytes) -> bytes:
    if len(value) > 32:
        raise ValueError("value longer than 32 bytes")
    return b"\x00" * (32 - len(value)) + value


def abi_encode_address(value: str) -> bytes:
    return _pad32(bytes.fromhex(normalize_address(value)[2:]))


def abi_encode_uint(value: int, bits: int = 256) -> bytes:
    if value < 0 or value >= (1 << bits):
        raise ValueError(f"uint{bits} out of range: {value}")
    return value.to_bytes(32, "big")


def abi_encode_int(value: int, bits: int = 24) -> bytes:
    min_v = -(1 << (bits - 1))
    max_v = (1 << (bits - 1)) - 1
    if value < min_v or value > max_v:
        raise ValueError(f"int{bits} out of range: {value}")
    return (value & ((1 << 256) - 1)).to_bytes(32, "big")


def uniswap_v4_pool_id(
    currency0: str,
    currency1: str,
    fee: int,
    tick_spacing: int,
    hooks: str,
) -> str:
    """PoolId = keccak256(abi.encode(currency0, currency1, fee, tickSpacing, hooks)).

    Callers must pass already-ordered currencies (uint160(currency0) < uint160(currency1),
    with native ETH as address(0)). This helper does not reorder.
    """
    c0 = normalize_address(currency0)
    c1 = normalize_address(currency1)
    if int(c0, 16) >= int(c1, 16):
        raise ValueError("currency0 must sort strictly before currency1")
    encoded = b"".join(
        [
            abi_encode_address(c0),
            abi_encode_address(c1),
            abi_encode_uint(fee, 24),
            abi_encode_int(tick_spacing, 24),
            abi_encode_address(hooks),
        ]
    )
    return "0x" + keccak256(encoded).hex()


def target_key(chain_id: Any, address: str) -> str:
    return f"{parse_chain_id(chain_id)}:{to_checksum_address(address)}"
