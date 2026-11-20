"""Config + path helpers shared by every module (already implemented)."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "config.yaml"


@lru_cache(maxsize=1)
def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def data_dir(kind: str) -> Path:
    """kind in {'raw', 'interim', 'processed'}; created on demand."""
    p = REPO_ROOT / load_config()["data_ingestion"]["paths"][f"{kind}_dir"]
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_raw(name: str) -> pd.DataFrame:
    """read_raw('player_standard') -> data/raw/fbref_player_standard.parquet"""
    return pd.read_parquet(data_dir("raw") / f"fbref_{name}.parquet")
