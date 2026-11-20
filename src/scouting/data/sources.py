"""Module 1b - Additional data sources.

The FBref tables you have contain NO xG/xA, passing, carrying, pressing or defensive-action data and
the schedule has no formations/lineups. The tactical-profile and role-fit work needs richer inputs.
`soccerdata` (already installed, v2026.43) wraps several other readers:

    Understat  read_player_season_stats / read_team_match_stats / read_shot_events   -> xG, xA, npxG, xGChain, xGBuildup, PPDA
    ESPN       read_lineup / read_matchsheet                                         -> starting XIs, formations
    WhoScored  read_events                                                           -> full event data (passes, pressures...) - heavy
    SoFIFA     read_player_ratings / read_team_ratings                               -> overall/potential, attribute ratings
    ClubElo    read_by_date                                                          -> opposition-strength adjustment

Not covered by soccerdata: market value, contract expiry, wages (Transfermarkt). Check the site's
terms before scraping; the config already assumes a `contract_expiry_cutoff_months` filter.

Verify each reader actually returns data for 2025-26 / 2026-27 BEFORE building on it.
"""
from __future__ import annotations

import pandas as pd


def fetch_understat_players() -> pd.DataFrame:
    """Player-season xG/xA/npxG/xGChain/xGBuildup for the Big 5. Cache to data/raw/understat_*.parquet."""
    raise NotImplementedError


def fetch_understat_team_matches() -> pd.DataFrame:
    """Match-level team xG, xGA, PPDA, deep completions. Basis for pressing/possession style features."""
    raise NotImplementedError


def fetch_lineups() -> pd.DataFrame:
    """One row per (match, team): formation + starting XI. Basis for 'which system does the team play'."""
    raise NotImplementedError


def fetch_market_data() -> pd.DataFrame:
    """player, club, market_value_eur, contract_expiry. Needed for budget/contract constraints."""
    raise NotImplementedError
