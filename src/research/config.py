"""Project paths and configuration.

Centralizes filesystem locations so notebooks and scripts don't hardcode paths.
Loads environment variables from a local .env file if present.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Repository root = two levels up from this file (src/research/config.py).
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

# Data directories (see README for the meaning of each stage).
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Optional API credentials, read from the environment (never commit real keys).
# An NCBI key raises Entrez rate limits; set it in .env as NCBI_API_KEY=...
NCBI_API_KEY = os.getenv("NCBI_API_KEY")
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "free2007free@gmail.com")
