"""Module 2 - Feature engineering: turn counting stats into comparable, role-aware numbers.

Core ideas to practise:
  * per-90 normalisation and minutes-based reliability (a striker with 3 goals in 90 min is noise)
  * empirical-Bayes / shrinkage of rates toward the position mean for low-minute players
  * percentile ranks *within position group and league* (not across all players)
  * league-strength adjustment (a goal in Ligue 1 != a goal in the Premier League) - ClubElo is one source
  * partial-season handling: blend 2526 (full) + 2627 (partial) with the time-decay in config
"""
from __future__ import annotations

import pandas as pd


def add_per90(df: pd.DataFrame, count_cols: list[str], minutes_col: str = "minutes") -> pd.DataFrame:
    """Add `<col>_p90` for each counting stat."""
    raise NotImplementedError


def shrink_rate(successes: pd.Series, exposure: pd.Series, prior_mean: float, prior_strength: float) -> pd.Series:
    """Empirical-Bayes shrinkage: (successes + prior_mean*k) / (exposure + k).

    Done when: a 90-minute outlier is pulled strongly toward the mean and a 3000-minute player barely moves.
    Stretch: estimate prior_mean/k from the data (method of moments on a Beta/Gamma prior).
    """
    raise NotImplementedError


def position_percentiles(df: pd.DataFrame, feature_cols: list[str], group_cols: list[str]) -> pd.DataFrame:
    """Percentile rank of every feature within each group (e.g. pos_primary x season)."""
    raise NotImplementedError


def blend_seasons(df: pd.DataFrame, decay: float) -> pd.DataFrame:
    """Weighted combination of a player's seasons: weight = minutes * decay**seasons_ago."""
    raise NotImplementedError


def minutes_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Apply preprocessing.min_minutes_* and age_range from config.yaml."""
    raise NotImplementedError
