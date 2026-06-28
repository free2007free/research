# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## Project overview

`research` is an **academic / literature research project** written in Python.
It supports searching, collecting, and analyzing scholarly literature (e.g. from
PubMed via Entrez) and recording the resulting analysis.

- **Name:** `research` (`free2007free/research`)
- **Default working directory:** `/home/user/research`
- **Language:** Python ≥ 3.10, packaged with `pyproject.toml` (setuptools).

## Directory layout

```
src/research/        Importable package
  config.py          Project paths + env-based configuration
  literature.py      PubMed / Entrez search + fetch helpers
  analysis.py        Pure analysis + plotting helpers (no network/I/O)
  ingest.py          Load a reading list (CSV/JSON) from data/external → Articles
  watch.py           Detect new/changed files across runs (content-hash ledger)
scripts/             Runnable example / pipeline scripts
  example_analysis.py  End-to-end: search → fetch → summarize → save outputs
  analyze_reading_list.py  Analyze a Drive-synced reading list from data/external
  integrate_monthly_reports.py  Cross-report integration of monthly reports
  process_new_reports.py  Idempotent: analyze only files new since the last run
tests/               Pytest suite (network calls mocked — runs offline)
notebooks/           Exploratory Jupyter notebooks
  example_analysis.ipynb  Demonstrates the workflow (has an offline section)
data/                raw → interim → processed → external pipeline (gitignored)
outputs/             Figures, tables, exported results (gitignored)
docs/                Notes and written documentation
pyproject.toml       Package metadata, dependencies, tool config
README.md            Human-facing quick start
```

The package lives under `src/` (src layout). Import it as `research`, e.g.
`from research.literature import search_pubmed`.

## Build / run / test

Use a virtual environment. Common commands:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,analysis]"   # install package + tooling

pytest                              # run tests
ruff check .                        # lint
ruff format .                       # format
mypy src                            # type-check
```

The test suite mocks all Entrez/network calls, so `pytest` must pass **without**
internet access. Keep it that way: never let a unit test hit the network.

## Conventions

- **Isolate network access.** All external API calls live in dedicated modules
  (e.g. `literature.py`). The rest of the code stays pure and testable.
- **No hardcoded paths.** Use the constants in `research.config` (`RAW_DIR`,
  `PROCESSED_DIR`, etc.) instead of literal paths in scripts/notebooks.
- **Data pipeline stages:** `raw` (immutable downloads) → `interim` (partial) →
  `processed` (analysis-ready). `external` holds third-party reference data.
  Contents are gitignored; only `.gitkeep` files are tracked — do not commit
  large or sensitive data.
- **Secrets** live in a local `.env` (gitignored); see `.env.example`. Never
  commit real API keys.
- **Style:** ruff (line length 100, rules E/F/I/UP/B). Add type hints; mypy runs
  over `src`.
- **Tests:** add a test under `tests/` for new functionality; mock the network.
- **External sources (e.g. Google Drive):** the package never calls Drive
  directly. Files from the Drive *journal reading* folder are synced into
  `data/external/` and read from there via `research.ingest`, keeping runtime
  code offline-testable and consistent with the data-pipeline convention.
- **Keep this file and `README.md` current** when structure or conventions change.

## Working principles

Operating guidelines for any assistant making changes here:

- **Read before writing** — read the relevant files before editing. (寫之前先讀檔案)
- **State assumptions when unsure** — if the request is ambiguous, say your
  assumption before acting. (不確定就先說假設)
- **Prefer the simplest change** — smaller diffs over clever ones. (改動越簡單越好)
- **Don't invent architecture** — follow the existing structure; don't fabricate
  one. (不要自己腦補架構)
- **Verify the output** — run the code or inspect results after a change. (做完要驗證輸出)
- **Understand before modifying** (先理解，再修改)
- **No gratuitous refactors** — don't rewrite the whole package to show off.
  (不要為了炫技重構整包)
- **Record repeated mistakes** — note recurring errors under *Known pitfalls* so
  they aren't repeated. (重複錯誤要記下來)
- **Every step must be explainable** — be able to justify each change. (每一步都要能解釋)
- **Run tests before delivering** — `pytest` must pass before handing off. (交付前先跑測試)

### Known pitfalls

- **Matplotlib + CJK labels render as boxes.** The default font lacks CJK glyphs,
  so charts with Chinese category names show tofu boxes and emit warnings.
  Romanize labels for plotting (see `scripts/integrate_monthly_reports.py`, which
  maps the specialty names to English before `.plot()`).

## Git workflow

- **Develop on the feature branch** `claude/claude-md-docs-slucre`. Create it
  locally if it does not exist. Do not push to any other branch without
  explicit permission.
- **Commit** with clear, descriptive messages.
- **Push** with `git push -u origin <branch-name>`. On network failure, retry up
  to 4 times with exponential backoff (2s, 4s, 8s, 16s).
- **Do not open a pull request** unless explicitly asked.
- When fetching/pulling, prefer specifying the branch: `git fetch origin <branch>`.
