"""Ingest a reading list from local reference files into ``Article`` records.

This is the bridge between files synced from the Google Drive *journal reading*
folder (downloaded into ``data/external/`` — see README) and the pure analysis
helpers in :mod:`research.analysis`.

Two formats are supported for a reading list:

* **CSV** with columns ``pmid, title, journal, year`` (extra columns ignored).
* **JSON** — a list of objects with the same keys.

Plain PDFs can also be *inventoried* (counted / listed by filename) via
:func:`list_pdf_titles`, since reliable metadata extraction from arbitrary PDFs
is out of scope here.

Everything in this module is offline and pure (filesystem reads only), so it is
covered by the unit tests without network access.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from research.config import EXTERNAL_DIR
from research.literature import Article

_FIELDS = ("pmid", "title", "journal", "year")


def _article_from_mapping(row: dict) -> Article:
    return Article(
        pmid=str(row.get("pmid", "")).strip(),
        title=str(row.get("title", "")).strip(),
        journal=str(row.get("journal", "")).strip(),
        year=str(row.get("year", "")).strip(),
    )


def load_reading_list_csv(path: str | Path) -> list[Article]:
    """Load a reading list from a CSV file with ``pmid/title/journal/year`` columns."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as fh:
        return [_article_from_mapping(row) for row in csv.DictReader(fh)]


def load_reading_list_json(path: str | Path) -> list[Article]:
    """Load a reading list from a JSON file (a list of article objects)."""
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return [_article_from_mapping(row) for row in data]


def load_reading_list(path: str | Path) -> list[Article]:
    """Load a reading list, dispatching on the file extension (.csv or .json)."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return load_reading_list_csv(path)
    if suffix == ".json":
        return load_reading_list_json(path)
    raise ValueError(f"Unsupported reading-list format: {suffix!r} (expected .csv or .json)")


def list_pdf_titles(directory: str | Path = EXTERNAL_DIR) -> list[str]:
    """Return PDF filenames (without extension) found in ``directory``.

    A lightweight inventory of papers when only the PDFs themselves are present.
    """
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(p.stem for p in directory.glob("*.pdf"))
