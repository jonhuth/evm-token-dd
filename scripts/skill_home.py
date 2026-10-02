"""Resolve this skill's install directory without hardcoded personal paths."""

from __future__ import annotations

import os
from pathlib import Path

ENV_HOME = "EVM_TOKEN_DD_HOME"


def skill_home() -> Path:
    """Directory that contains SKILL.md.

    Order: $EVM_TOKEN_DD_HOME, then two levels above this file (scripts/ → package).
    """
    override = os.environ.get(ENV_HOME)
    if override:
        path = Path(override).expanduser().resolve()
        _require_skill_md(path, source=f"${ENV_HOME}")
        return path
    path = Path(__file__).resolve().parent.parent
    _require_skill_md(path, source="package-relative")
    return path


def _require_skill_md(path: Path, *, source: str) -> None:
    skill = path / "SKILL.md"
    if not skill.is_file():
        raise FileNotFoundError(
            f"Cannot resolve skill home from {source}: {path} has no SKILL.md. "
            f"Set {ENV_HOME} to the evm-token-due-diligence directory."
        )


def scripts_dir() -> Path:
    return skill_home() / "scripts"


def schemas_dir() -> Path:
    return skill_home() / "schemas"


def fixtures_dir() -> Path:
    return skill_home() / "tests" / "fixtures"
