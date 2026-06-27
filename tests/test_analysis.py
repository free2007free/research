"""Offline tests for the analysis helpers."""

from research.analysis import publications_per_year, summarize, top_journals
from research.literature import Article


def _articles() -> list[Article]:
    return [
        Article(pmid="1", title="A", journal="Nature", year="2022"),
        Article(pmid="2", title="B", journal="Nature", year="2024"),
        Article(pmid="3", title="C", journal="Cell", year="2024"),
        Article(pmid="4", title="D", journal="Cell", year=""),  # bad year ignored
    ]


def test_publications_per_year_counts_and_sorts():
    assert publications_per_year(_articles()) == {2022: 1, 2024: 2}


def test_top_journals_orders_by_frequency():
    assert top_journals(_articles(), n=2) == [("Nature", 2), ("Cell", 2)]


def test_summarize_reports_span_and_total():
    summary = summarize(_articles())
    assert summary["n_articles"] == 4
    assert summary["years_covered"] == (2022, 2024)
