"""Module 1a - Cleaning raw FBref tables into one analysis-ready player-season table.

Known problems in the current raw data (found in review, see docs/ROADMAP.md):
  * Bundesliga rows have league == <NA> in every player/team table (929 player rows).
  * Players who moved clubs mid-season appear once per club (149 in 2526).
  * 2627 is a partial season (~12 matches), 2526 is complete.
  * Raw `pos` is a messy string ("FW,MF", "MF,DF"): first token = primary position.
"""
from __future__ import annotations

import pandas as pd

KEYS = ["league", "season", "team", "player"]


def fix_missing_league(df: pd.DataFrame, schedules: pd.DataFrame) -> pd.DataFrame:
    """Fill NA `league` by mapping team -> league using the schedules table.

    Done when: no NA league remains in any raw table; Bundesliga teams are 'GER-Bundesliga'.
    Hint: schedules has (league, home_team) pairs. Beware FBref team-name spellings.
    """
    raise NotImplementedError


def normalise_positions(df: pd.DataFrame) -> pd.DataFrame:
    """Add `pos_primary` (GK/DF/MF/FW) and `pos_secondary` (or NA) from raw `pos`.

    Later (Module 4) you will refine these into tactical roles (CB, FB, DM, CM, AM, W, ST).
    """
    raise NotImplementedError


def merge_player_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Join standard/shooting/misc/playing_time on KEYS (+born) into one wide table.

    Watch out for: duplicate column names across tables, `keeper` being GK-only
    (left join), and column names with '%' or '/' - rename to snake_case.
    """
    raise NotImplementedError


def aggregate_multi_club(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse mid-season transfers into one row per (season, player) *for ranking purposes*
    while keeping the per-club rows available (needed for team-fit analysis).

    Decide + document: sum counting stats, recompute rates from totals (never average rates!).
    """
    raise NotImplementedError


def build_player_season_table() -> pd.DataFrame:
    """Orchestrate the steps above and write data/interim/player_season.parquet."""
    raise NotImplementedError
