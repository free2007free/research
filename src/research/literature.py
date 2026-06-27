"""Helpers for searching and fetching scholarly literature from PubMed.

Thin wrapper around Biopython's Entrez API. Keep network access isolated here so
the rest of the codebase stays testable and offline-friendly.

Example
-------
>>> from research.literature import search_pubmed, fetch_summaries
>>> ids = search_pubmed("CRISPR off-target", retmax=5)
>>> records = fetch_summaries(ids)
"""

from __future__ import annotations

from dataclasses import dataclass

from Bio import Entrez

from research.config import NCBI_API_KEY, NCBI_EMAIL

Entrez.email = NCBI_EMAIL
if NCBI_API_KEY:
    Entrez.api_key = NCBI_API_KEY


@dataclass
class Article:
    """A minimal representation of a PubMed article."""

    pmid: str
    title: str
    journal: str
    year: str


def search_pubmed(query: str, retmax: int = 20) -> list[str]:
    """Return a list of PubMed IDs (PMIDs) matching ``query``."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    try:
        record = Entrez.read(handle)
    finally:
        handle.close()
    return list(record.get("IdList", []))


def fetch_summaries(pmids: list[str]) -> list[Article]:
    """Fetch summary metadata for the given PMIDs."""
    if not pmids:
        return []
    handle = Entrez.esummary(db="pubmed", id=",".join(pmids))
    try:
        records = Entrez.read(handle)
    finally:
        handle.close()

    articles: list[Article] = []
    for rec in records:
        articles.append(
            Article(
                pmid=str(rec.get("Id", "")),
                title=str(rec.get("Title", "")),
                journal=str(rec.get("FullJournalName", "")),
                year=str(rec.get("PubDate", "")).split(" ")[0],
            )
        )
    return articles
