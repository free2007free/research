#!/usr/bin/env python
"""Integrate the monthly literature reports synced from Google Drive.

Reads the unified reading list (data/external/reading_list.csv, with columns
pmid,title,journal,year,report,section,topic), then prints a cross-report
breakdown and writes summary charts to outputs/.

Usage
-----
    python scripts/integrate_monthly_reports.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from research.config import EXTERNAL_DIR, OUTPUTS_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=str(EXTERNAL_DIR / "reading_list.csv"),
        help="Unified reading-list CSV (default: data/external/reading_list.csv)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"No reading list at {path}. Sync the Drive reports first.")
        return

    df = pd.read_csv(path, dtype={"pmid": str}).fillna({"pmid": ""})
    unique = df.drop_duplicates(subset="pmid").loc[lambda d: d["pmid"] != ""]
    n_blank = (df["pmid"] == "").sum()
    n_unique = len(unique) + n_blank

    print(f"Total rows: {len(df)}  |  unique papers (by PMID): {n_unique}")
    print("\nBy report x section:")
    print(df.pivot_table(index="report", columns="section", values="pmid",
                         aggfunc="count", fill_value=0, margins=True, margins_name="總計"))

    print("\nCross-report duplicates (same PMID in >1 report):")
    dups = df[df["pmid"] != ""].groupby("pmid").filter(lambda g: g["report"].nunique() > 1)
    for pmid, g in dups.groupby("pmid"):
        print(f"  {pmid}: {', '.join(g['report'])} — {g['title'].iloc[0][:60]}")

    print("\nTop journals (unique papers):")
    print(unique["journal"].value_counts().head(12).to_string())

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # Romanize specialty names so the chart renders without a CJK font.
    report_en = {"ERCP": "ERCP", "肝硬化": "Cirrhosis", "脂肪肝": "Fatty liver"}
    plot_df = df.assign(report=df["report"].map(report_en).fillna(df["report"]))
    ax = plot_df.pivot_table(index="report", columns="section", values="pmid",
                             aggfunc="count", fill_value=0).plot(kind="bar", figsize=(7, 4))
    ax.set_ylabel("Papers")
    ax.set_title("2026-05 monthly reports: papers by specialty x section")
    fig = ax.get_figure()
    fig.tight_layout()
    p1 = OUTPUTS_DIR / "monthly_by_report_section.png"
    fig.savefig(p1, dpi=150)
    print(f"\nWrote {p1}")

    ax2 = unique["journal"].value_counts().head(12).iloc[::-1].plot(
        kind="barh", figsize=(7, 5), color="#4C72B0")
    ax2.set_xlabel("Unique papers")
    ax2.set_title("2026-05 monthly reports: top journals")
    fig2 = ax2.get_figure()
    fig2.tight_layout()
    p2 = OUTPUTS_DIR / "monthly_top_journals.png"
    fig2.savefig(p2, dpi=150)
    print(f"Wrote {p2}")


if __name__ == "__main__":
    main()
