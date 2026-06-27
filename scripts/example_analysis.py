#!/usr/bin/env python
"""Example end-to-end literature analysis.

Searches PubMed for a query, fetches article summaries, prints a small summary,
and saves a publications-per-year chart plus a CSV of the records to outputs/.

Usage
-----
    python scripts/example_analysis.py "CRISPR off-target" --retmax 50

Requires network access (and ideally an NCBI_API_KEY in .env). The analysis and
plotting logic itself is covered by offline unit tests in tests/.
"""

from __future__ import annotations

import argparse
import csv
import json

from research.analysis import plot_publications_per_year, summarize
from research.config import OUTPUTS_DIR
from research.literature import fetch_summaries, search_pubmed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("--retmax", type=int, default=50, help="Max records to fetch")
    args = parser.parse_args()

    print(f"Searching PubMed for: {args.query!r}")
    pmids = search_pubmed(args.query, retmax=args.retmax)
    print(f"  found {len(pmids)} PMIDs; fetching summaries...")
    articles = fetch_summaries(pmids)

    summary = summarize(articles)
    print(json.dumps(summary, indent=2, default=str))

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUTS_DIR / "articles.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["pmid", "year", "journal", "title"])
        for art in articles:
            writer.writerow([art.pmid, art.year, art.journal, art.title])
    print(f"Wrote {csv_path}")

    fig = plot_publications_per_year(articles)
    fig_path = OUTPUTS_DIR / "publications_per_year.png"
    fig.savefig(fig_path, dpi=150)
    print(f"Wrote {fig_path}")


if __name__ == "__main__":
    main()
