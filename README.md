# research

An academic / literature research project. The codebase supports searching,
collecting, and analyzing scholarly literature (e.g. via PubMed) and recording
the analysis.

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install the package (editable) with dev + analysis extras
pip install -e ".[dev,analysis]"

# 3. Configure credentials (optional but recommended for PubMed)
cp .env.example .env             # then edit .env

# 4. Run the tests
pytest
```

## Usage

```python
from research.literature import search_pubmed, fetch_summaries

pmids = search_pubmed("CRISPR off-target effects", retmax=10)
for article in fetch_summaries(pmids):
    print(article.year, article.title)
```

### Example analysis

An end-to-end example searches PubMed, summarizes the results, and writes a CSV
plus a publications-per-year chart to `outputs/`:

```bash
python scripts/example_analysis.py "CRISPR off-target effects" --retmax 50
```

See `notebooks/example_analysis.ipynb` for the same workflow as a notebook
(including an offline section that runs without network access).

### Analyzing a reading list (Google Drive)

Papers collected in a Google Drive *journal reading* folder can be analyzed too.
The project code does not talk to Drive directly; instead, files are synced into
`data/external/` and read from there:

1. The assistant downloads the Drive folder's contents into `data/external/`
   (via its Drive connection), or you place a reading-list `reading_list.csv`
   / `.json` there yourself. CSV columns: `pmid,title,journal,year`.
2. Run the analysis:

   ```bash
   python scripts/analyze_reading_list.py data/external/reading_list.csv
   ```

   It prints a summary and writes `outputs/reading_list_per_year.png`. With no
   reading list present it inventories any PDFs in `data/external/` instead.

For multiple monthly reports across specialties, `integrate_monthly_reports.py`
produces a cross-report breakdown (counts by specialty/section, top journals,
duplicate detection) and charts. A worked example covering the 2026-05 reports
is committed at `docs/literature_monthly_2026-05.md`.

   ```bash
   python scripts/integrate_monthly_reports.py
   ```

## Project layout

```
research/
├── src/research/        # Importable Python package
│   ├── config.py        # Paths + env-based configuration
│   ├── literature.py    # PubMed / Entrez search + fetch helpers
│   └── analysis.py      # Pure analysis + plotting helpers
├── scripts/             # Runnable example / pipeline scripts
├── tests/               # Pytest suite (network calls are mocked)
├── notebooks/           # Exploratory Jupyter notebooks
├── data/
│   ├── raw/             # Original, immutable downloads (gitignored)
│   ├── interim/         # Intermediate, partially processed data (gitignored)
│   ├── processed/       # Final, analysis-ready datasets (gitignored)
│   └── external/        # Third-party reference data (gitignored)
├── outputs/             # Figures, tables, exported results (gitignored)
├── docs/                # Notes and written documentation
├── pyproject.toml       # Package metadata, dependencies, tool config
└── CLAUDE.md            # Guidance for AI assistants
```

The `data/` subdirectories follow a raw → interim → processed pipeline. Their
contents are gitignored; only `.gitkeep` placeholders are tracked, so the
structure persists without committing large or sensitive files.

## Development

```bash
ruff check .         # lint
ruff format .        # format
mypy src             # type-check
pytest               # test
```

## Configuration

Runtime configuration is read from a local `.env` file (see `.env.example`).
Secrets must never be committed — `.env` is gitignored.
