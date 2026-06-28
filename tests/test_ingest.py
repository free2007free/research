"""Offline tests for the reading-list ingestion helpers."""

import json

import pytest

from research.ingest import (
    list_pdf_titles,
    load_reading_list,
    load_reading_list_csv,
    load_reading_list_json,
)
from research.literature import Article


def test_load_reading_list_csv(tmp_path):
    csv_path = tmp_path / "reading.csv"
    csv_path.write_text(
        "pmid,title,journal,year\n111,A study,Nature,2024\n", encoding="utf-8"
    )
    assert load_reading_list_csv(csv_path) == [
        Article(pmid="111", title="A study", journal="Nature", year="2024")
    ]


def test_load_reading_list_json(tmp_path):
    json_path = tmp_path / "reading.json"
    json_path.write_text(
        json.dumps([{"pmid": "222", "title": "B", "journal": "Cell", "year": "2023"}]),
        encoding="utf-8",
    )
    assert load_reading_list_json(json_path) == [
        Article(pmid="222", title="B", journal="Cell", year="2023")
    ]


def test_load_reading_list_dispatches_on_extension(tmp_path):
    csv_path = tmp_path / "r.csv"
    csv_path.write_text("pmid,title,journal,year\n1,T,J,2020\n", encoding="utf-8")
    assert load_reading_list(csv_path)[0].pmid == "1"


def test_load_reading_list_rejects_unknown_format(tmp_path):
    bad = tmp_path / "r.txt"
    bad.write_text("nope", encoding="utf-8")
    with pytest.raises(ValueError):
        load_reading_list(bad)


def test_list_pdf_titles(tmp_path):
    (tmp_path / "Smith2024_CRISPR.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "notes.txt").write_text("ignore me", encoding="utf-8")
    assert list_pdf_titles(tmp_path) == ["Smith2024_CRISPR"]


def test_list_pdf_titles_missing_dir_returns_empty(tmp_path):
    assert list_pdf_titles(tmp_path / "does-not-exist") == []
