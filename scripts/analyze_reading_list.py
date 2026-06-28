#!/usr/bin/env python
"""Analyze a reading list synced from the Google Drive 'journal reading' folder.

Workflow:
    1. Files from the Drive folder are downloaded into data/external/ (the
       assistant does this via its Drive connection; see README).
    2. This script loads a reading-list CSV/JSON from there, summarizes it, and
       writes a publications-per-year chart to outputs/.

Usage
-----
    python scripts/analyze_reading_list.py data/external/reading_list.csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from research.analysis import plot_publications_per_year, summarize
from research.config import EXTERNAL_DIR, OUTPUTS_DIR
from research.ingest import list_pdf_titles, load_reading_list


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=str(EXTERNAL_DIR / "reading_list.csv"),
        help="Reading-list CSV or JSON (default: data/external/reading_list.csv)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        pdfs = list_pdf_titles(EXTERNAL_DIR)
        print(f"No reading list at {path}.")
        if pdfs:
            print(f"Found {len(pdfs)} PDF(s) in {EXTERNAL_DIR}:")
            for name in pdfs:
                print(f"  - {name}")
        else:
            print(f"Place a reading-list CSV/JSON or PDFs in {EXTERNAL_DIR} first.")
        return

    articles = load_reading_list(path)
    print(f"Loaded {len(articles)} articles from {path}")
    print(json.dumps(summarize(articles), indent=2, default=str))

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    fig = plot_publications_per_year(articles)
    fig_path = OUTPUTS_DIR / "reading_list_per_year.png"
    fig.savefig(fig_path, dpi=150)
    print(f"Wrote {fig_path}")


if __name__ == "__main__":
    main()
