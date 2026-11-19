import logging
import time
from pathlib import Path
from typing import List, Optional

import pandas as pd
import soccerdata as sd
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FBrefLoader:
    """Handles data extraction from FBref via soccerdata and caches raw Parquet files."""

    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        ingestion_cfg = self.config["data_ingestion"]
        self.leagues: List[str] = ingestion_cfg["leagues"]
        self.seasons: List[str] = ingestion_cfg["seasons"]
        self.player_stat_types: List[str] = ingestion_cfg["player_stat_types"]
        self.team_stat_types: List[str] = ingestion_cfg["team_stat_types"]
        self.team_stat_season_types: List[str] = ingestion_cfg["team_stat_season_types"]
        self.raw_dir = Path(ingestion_cfg["paths"]["raw_dir"])
        self.raw_dir.mkdir(parents=True, exist_ok=True)

        self.fbref = sd.FBref(leagues=self.leagues, seasons=self.seasons)

    @staticmethod
    def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Flattens MultiIndex headers into single snake_case-friendly strings."""
        df = df.reset_index()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                "_".join([str(c).strip() for c in col if str(c).strip() and not str(c).startswith("Unnamed")])
                for col in df.columns.values
            ]
        return df
    
    @staticmethod
    def _sanitize_for_parquet(df: pd.DataFrame) -> pd.DataFrame:
        """Normalizes mixed-type FBref columns so PyArrow serialization never fails."""
        df = df.copy()

        # 1. Handle FBref's 'YY-DDD' age format (e.g., '29-041' -> 29.11)
        if "age" in df.columns:
            age_parts = df["age"].astype("string").str.split("-", expand=True)
            years = pd.to_numeric(age_parts[0], errors="coerce")
            days = pd.to_numeric(age_parts[1], errors="coerce").fillna(0) if age_parts.shape[1] > 1 else 0
            df["age"] = (years + (days / 365.25)).round(2)

        # 2. Known categorical/identifier columns to preserve as clean strings
        text_cols = {
            "league", "season", "team", "player", "nation", "pos",
            "comp", "round", "day", "venue", "result", "opponent",
            "captain", "formation", "opp_formation", "referee", "match_report", "notes", "date", "time"
        }

        for col in df.columns:
            col_lower = col.lower()
            if col_lower in text_cols or any(k in col_lower for k in ["player", "team", "nation", "pos", "url", "report"]):
                df[col] = df[col].astype("string")
                continue

            # 3. Strip thousands commas and coerce numeric stat columns safely
            if df[col].dtype == "object" or pd.api.types.is_string_dtype(df[col]):
                cleaned = df[col].astype("string").str.replace(",", "", regex=False).str.strip()
                converted = pd.to_numeric(cleaned, errors="coerce")
                # Only overwrite with numeric if it didn't wipe valid non-null text into all-NaN
                if converted.notna().sum() >= cleaned.notna().sum() * 0.8:
                    df[col] = converted
                else:
                    df[col] = cleaned.astype("string")

        return df

    def _save_or_load(
        self,
        filename: str,
        fetch_fn,
        force_refresh: bool = False,
        sleep_sec: float = 3.0,
    ) -> pd.DataFrame:
        """Loads cached Parquet if present; otherwise executes fetch_fn and persists."""
        file_path = self.raw_dir / filename

        if file_path.exists() and not force_refresh:
            logger.info(f"Loading cached data from {file_path}")
            return pd.read_parquet(file_path)

        logger.info(f"Fetching fresh data for {filename}...")
        df = fetch_fn()
        df = self._flatten_columns(df)
        df = self._sanitize_for_parquet(df)
        df.to_parquet(file_path, index=False)
        logger.info(f"Saved {len(df)} rows to {file_path}")

        time.sleep(sleep_sec)
        return df

    def fetch_player_season_stats(self, force_refresh: bool = False) -> dict[str, pd.DataFrame]:
        """Pulls all configured player season stat tables."""
        tables = {}
        for stat_type in self.player_stat_types:
            filename = f"fbref_player_{stat_type}.parquet"
            tables[stat_type] = self._save_or_load(
                filename=filename,
                fetch_fn=lambda st=stat_type: self.fbref.read_player_season_stats(stat_type=st),
                force_refresh=force_refresh,
            )
        return tables

    def fetch_team_season_stats(self, force_refresh: bool = False) -> dict[str, pd.DataFrame]:
        """Pulls all configured team season stat tables for league benchmarking."""
        tables = {}
        for stat_type in self.team_stat_season_types:
            filename = f"fbref_team_{stat_type}.parquet"
            tables[stat_type] = self._save_or_load(
                filename=filename,
                fetch_fn=lambda st=stat_type: self.fbref.read_team_season_stats(stat_type=st),
                force_refresh=force_refresh,
            )
        return tables

    def fetch_schedules(self, force_refresh: bool = False) -> pd.DataFrame:
        """Pulls match schedules, dates, and formations across configured leagues."""
        return self._save_or_load(
            filename="fbref_schedules.parquet",
            fetch_fn=self.fbref.read_schedule,
            force_refresh=force_refresh,
        )

    def fetch_team_match_stats(
        self,
        stat_type: str = "passing",
        opponent_stats: bool = False,
        force_refresh: bool = False,
    ) -> pd.DataFrame:
        """Pulls match-by-match team stats (useful for manager tactical profiling)."""
        suffix = "opp" if opponent_stats else "team"
        filename = f"fbref_match_{suffix}_{stat_type}.parquet"
        return self._save_or_load(
            filename=filename,
            fetch_fn=lambda: self.fbref.read_team_match_stats(
                stat_type=stat_type, opponent_stats=opponent_stats
            ),
            force_refresh=force_refresh,
        )

    def run_full_ingestion(self, force_refresh: bool = False) -> None:
        """Executes full raw ingestion pipeline and caches all tables to data/raw/."""
        logger.info("Starting FBref ingestion for leagues: %s", self.leagues)
        self.fetch_player_season_stats(force_refresh=force_refresh)
        self.fetch_team_season_stats(force_refresh=force_refresh)
        self.fetch_schedules(force_refresh=force_refresh)

        # Pull core match logs needed for pressing/build-up tactical diagnostics
        for st in ["schedule", "shooting", "misc"]:
            self.fetch_team_match_stats(stat_type=st, opponent_stats=False, force_refresh=force_refresh)
            self.fetch_team_match_stats(stat_type=st, opponent_stats=True, force_refresh=force_refresh)

        logger.info("FBref raw ingestion complete.")


if __name__ == "__main__":
    loader = FBrefLoader(config_path="config/config.yaml")
    loader.run_full_ingestion(force_refresh=False)


