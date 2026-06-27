"""Analysis helpers for collections of literature records.

These functions are pure (no network, no I/O) so they're easy to test and reuse
from scripts or notebooks. Plotting helpers return a Matplotlib figure rather
than showing or saving it, leaving that decision to the caller.
"""

from __future__ import annotations

from collections import Counter

from research.literature import Article


def publications_per_year(articles: list[Article]) -> dict[int, int]:
    """Count publications per year, sorted ascending by year.

    Articles whose year is missing or non-numeric are ignored.
    """
    counts: Counter[int] = Counter()
    for art in articles:
        try:
            counts[int(art.year)] += 1
        except (TypeError, ValueError):
            continue
    return dict(sorted(counts.items()))


def top_journals(articles: list[Article], n: int = 10) -> list[tuple[str, int]]:
    """Return the ``n`` most frequent journals as (journal, count) pairs."""
    counts = Counter(art.journal for art in articles if art.journal)
    return counts.most_common(n)


def summarize(articles: list[Article]) -> dict[str, object]:
    """Produce a small summary dict for a set of articles."""
    by_year = publications_per_year(articles)
    return {
        "n_articles": len(articles),
        "years_covered": (min(by_year), max(by_year)) if by_year else None,
        "publications_per_year": by_year,
        "top_journals": top_journals(articles, n=5),
    }


def plot_publications_per_year(articles: list[Article]):
    """Return a Matplotlib bar-chart figure of publications per year.

    Importing Matplotlib lazily keeps it an optional dependency for callers that
    only need the non-plotting helpers.
    """
    import matplotlib.pyplot as plt

    by_year = publications_per_year(articles)
    fig, ax = plt.subplots(figsize=(8, 4))
    if by_year:
        ax.bar(list(by_year.keys()), list(by_year.values()), color="#4C72B0")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of publications")
    ax.set_title("Publications per year")
    fig.tight_layout()
    return fig
