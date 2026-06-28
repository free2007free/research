"""Offline tests for new-file detection (research.watch)."""

from research.watch import find_unprocessed, load_ledger, mark_processed, save_ledger


def _write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def test_find_unprocessed_treats_all_as_new_without_ledger(tmp_path):
    _write(tmp_path / "a.csv", "x")
    _write(tmp_path / "b.json", "[]")
    found = {p.name for p in find_unprocessed(tmp_path, ledger={})}
    assert found == {"a.csv", "b.json"}


def test_find_unprocessed_skips_recorded_files(tmp_path):
    f = _write(tmp_path / "a.csv", "x")
    ledger = mark_processed({}, [f])
    assert find_unprocessed(tmp_path, ledger) == []


def test_find_unprocessed_detects_changed_content(tmp_path):
    f = _write(tmp_path / "a.csv", "x")
    ledger = mark_processed({}, [f])
    _write(f, "x changed")  # same name, new content -> should resurface
    assert [p.name for p in find_unprocessed(tmp_path, ledger)] == ["a.csv"]


def test_find_unprocessed_ignores_hidden_files(tmp_path):
    _write(tmp_path / ".processed_ledger.json", "{}")
    _write(tmp_path / "a.csv", "x")
    assert [p.name for p in find_unprocessed(tmp_path, ledger={})] == ["a.csv"]


def test_ledger_roundtrip(tmp_path):
    f = _write(tmp_path / "a.csv", "x")
    ledger_path = tmp_path / ".processed_ledger.json"
    save_ledger(mark_processed({}, [f]), ledger_path)
    assert "a.csv" in load_ledger(ledger_path)


def test_find_unprocessed_missing_dir_returns_empty(tmp_path):
    assert find_unprocessed(tmp_path / "nope", ledger={}) == []
