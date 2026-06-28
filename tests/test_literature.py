"""Offline tests for the literature module.

Network calls to Entrez are mocked so the suite runs without internet access.
"""

from unittest.mock import patch

from research.literature import Article, fetch_summaries, search_pubmed


def test_search_pubmed_returns_id_list():
    fake = {"IdList": ["111", "222"]}
    with (
        patch("research.literature.Entrez.esearch"),
        patch("research.literature.Entrez.read", return_value=fake),
    ):
        assert search_pubmed("anything") == ["111", "222"]


def test_fetch_summaries_empty_input_skips_network():
    # Must not touch the network when given no PMIDs.
    with patch("research.literature.Entrez.esummary") as esummary:
        assert fetch_summaries([]) == []
        esummary.assert_not_called()


def test_fetch_summaries_maps_fields():
    fake = [
        {
            "Id": "111",
            "Title": "A study",
            "FullJournalName": "Nature",
            "PubDate": "2024 Jan 1",
        }
    ]
    with (
        patch("research.literature.Entrez.esummary"),
        patch("research.literature.Entrez.read", return_value=fake),
    ):
        (article,) = fetch_summaries(["111"])
        assert article == Article(pmid="111", title="A study", journal="Nature", year="2024")
