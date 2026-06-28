#!/usr/bin/env python
"""Analyze any new files that have arrived in data/external/ since the last run.

Idempotent automation unit: detects new or changed report files via a content
ledger, analyzes the new ones, regenerates the cross-report integration over the
full reading list, then records what it processed so the next run only picks up
genuinely new arrivals.

This is the building block for "analyze whenever a new file is received": run it
after syncing the Drive *journal reading* folder into data/external/ (manually,
or from a scheduled job).

Usage
-----
    python scripts/process_new_reports.py            # process new arrivals
    python scripts/process_new_reports.py --all      # ignore ledger, reprocess
    python scripts/process_new_reports.py --dry-run   # list new files only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from research.config import EXTERNAL_DIR
from research.ingest import load_reading_list
from research.watch import (
    DEFAULT_LEDGER,
    find_unprocessed,
    load_ledger,
    mark_processed,
    save_ledger,
)

SCRIPTS = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Reprocess every file, ignoring the ledger")
    parser.add_argument("--dry-run", action="store_true", help="List new files without analyzing")
    args = parser.parse_args()

    ledger = {} if args.all else load_ledger(DEFAULT_LEDGER)
    new_files = find_unprocessed(EXTERNAL_DIR, ledger)

    if not new_files:
        print(f"No new files in {EXTERNAL_DIR}. Nothing to do.")
        return 0

    print(f"New/changed files ({len(new_files)}):")
    for path in new_files:
        print(f"  - {path.name}")
    if args.dry_run:
        return 0

    # Per-file: summarize reading lists we can parse; other formats are just noted.
    for path in new_files:
        if path.suffix.lower() in {".csv", ".json"}:
            try:
                articles = load_reading_list(path)
                print(f"\n{path.name}: parsed {len(articles)} articles")
            except Exception as exc:  # noqa: BLE001 - report and continue
                print(f"\n{path.name}: could not parse as a reading list ({exc})")
        else:
            print(f"\n{path.name}: {path.suffix} report noted (convert to reading_list.csv to analyze)")

    # Regenerate the cross-report integration over the full reading list.
    reading_list = EXTERNAL_DIR / "reading_list.csv"
    if reading_list.exists():
        print("\nRegenerating cross-report integration...")
        subprocess.run(
            [sys.executable, str(SCRIPTS / "integrate_monthly_reports.py")], check=True
        )

    save_ledger(mark_processed(ledger, new_files), DEFAULT_LEDGER)
    print(f"\nLedger updated ({DEFAULT_LEDGER.name}). {len(new_files)} file(s) marked processed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
