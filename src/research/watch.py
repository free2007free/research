"""Detect newly-arrived or changed files in a directory across runs.

A tiny content-hash ledger so an automation step can answer "which files are
new since I last looked?" and process only those. Pure filesystem + JSON, no
network — covered by offline unit tests.

The ledger maps ``filename -> sha256`` and lives next to the watched files
(default ``data/external/.processed_ledger.json``). A file counts as
*unprocessed* when its name is absent from the ledger or its content hash
differs from the recorded one (i.e. it was re-uploaded / edited).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from research.config import EXTERNAL_DIR

DEFAULT_LEDGER = EXTERNAL_DIR / ".processed_ledger.json"
DEFAULT_PATTERNS = ("*.csv", "*.json", "*.xlsx", "*.md")


def file_digest(path: str | Path) -> str:
    """Return the SHA-256 hex digest of a file's bytes."""
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_ledger(ledger_path: str | Path = DEFAULT_LEDGER) -> dict[str, str]:
    """Load the processed-files ledger, returning an empty dict if absent."""
    path = Path(ledger_path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(ledger: dict[str, str], ledger_path: str | Path = DEFAULT_LEDGER) -> None:
    """Persist the ledger as pretty JSON, creating parent dirs as needed."""
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")


def find_unprocessed(
    directory: str | Path = EXTERNAL_DIR,
    ledger: dict[str, str] | None = None,
    patterns: tuple[str, ...] = DEFAULT_PATTERNS,
) -> list[Path]:
    """Return files in ``directory`` that are new or changed vs ``ledger``.

    ``ledger`` defaults to an empty mapping (everything counts as new). The
    ledger's own dotfile and other hidden files are ignored.
    """
    directory = Path(directory)
    ledger = {} if ledger is None else ledger
    if not directory.exists():
        return []

    seen: set[Path] = set()
    new: list[Path] = []
    for pattern in patterns:
        for path in sorted(directory.glob(pattern)):
            if path in seen or path.name.startswith("."):
                continue
            seen.add(path)
            if ledger.get(path.name) != file_digest(path):
                new.append(path)
    return new


def mark_processed(ledger: dict[str, str], paths: list[Path]) -> dict[str, str]:
    """Return a new ledger with ``paths`` recorded at their current digest."""
    updated = dict(ledger)
    for path in paths:
        updated[Path(path).name] = file_digest(path)
    return updated
