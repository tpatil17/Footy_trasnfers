"""MODULE 1b - SOURCES: fetch the extra data FBref does not have.

WHY THIS MODULE EXISTS
    Your FBref files contain no xG/xA, passing, pressing or defending data, and no formations or
    lineups. Without those you cannot answer "what system does United play?" (Module 3) or judge
    defenders and midfielders properly (Modules 4-5). This module adds the missing data.

WHAT YOU DO (same pattern for each function)
    1. Call the soccerdata reader for the same leagues/seasons as config.yaml.
    2. Flatten the columns and cache to data/raw/<source>_<table>.parquet, exactly like
       src/data/scripts/Fbreif_Loader.py does (reuse its _flatten_columns / _save_or_load ideas).
    3. Check coverage BEFORE building on it (see HOW TO TEST). Some sources may not have 2026-27 yet.

HELPFUL soccerdata READERS (installed, v2026.43)
    Understat  read_player_season_stats / read_team_match_stats / read_shot_events -> xG, xA, npxG, PPDA
    ESPN       read_lineup                                                         -> starting XI, formation
    SoFIFA     read_player_ratings                                                 -> overall / potential
    ClubElo    read_by_date  (BROKEN since Sept 2026: API behind auth, soccerdata issue #977)
    Full ratings of every free source, what worked and what did not: docs/DATASETS.md
    Not available in soccerdata: market value, contract expiry (Transfermarkt). Check the site's terms
    before scraping, or find another dataset.

RECOMMENDED ORDER   fetch_understat_players first - it has the highest value for the least effort.

HOW TO RUN / TEST   `python -c "from scouting.data.sources import fetch_understat_players as f; print(f().shape)"`
    (fetching is slow and rate-limited: the second run should be instant because of the cache).
"""
from __future__ import annotations

import pandas as pd


def fetch_understat_players() -> pd.DataFrame:
    """Player-season xG/xA/npxG/xGChain/xGBuildup for the Big 5.

    GOAL     Add shot-quality and chance-creation data FBref lacks (xG tells you if a striker is lucky).
    OUTPUT   one row per player-club-season; cached at data/raw/understat_player_season.parquet.

    HOW TO TEST
        df = fetch_understat_players()
        df.groupby(["league", "season"]).size()
        df[df.player.str.contains("Bruno Fernandes")]

    EXPECTED RESULT
        all 5 leagues for 2526 (complete) and 2627 (partial) present; columns include xG, xA, npxG;
        roughly the same number of players as player_standard (about 2800 in 2526) - exact match is
        NOT expected, names differ (see identity.py). Bruno Fernandes shows plausible xG/xA values.
        If a league/season is empty, note it in docs/ROADMAP.md and decide how to handle it.
    """
    raise NotImplementedError


def fetch_understat_team_matches() -> pd.DataFrame:
    """Match-level team xG, xGA, PPDA, deep completions.

    GOAL     Basis for the style vector in Module 3: pressing (PPDA), chance quality, attack/defence balance.
    OUTPUT   one row per (match, team); cached at data/raw/understat_team_match.parquet.

    HOW TO TEST
        df = fetch_understat_team_matches()
        df[df.team.str.contains("Manchester")].groupby("season").size()

    EXPECTED RESULT
        Manchester United rows = number of matches played (38 for 2526; about 12 so far in 2627);
        every row has xG, xGA and PPDA values (no mass of NA); the league's average PPDA is roughly 9-13 (lower = more pressing).
    """
    raise NotImplementedError


def fetch_lineups() -> pd.DataFrame:
    """Starting XI + formation for every match.

    GOAL     Learn which formation(s) United actually uses and which player fills which role slot.
    OUTPUT   one row per (match, team) with `formation` and the 11 starters; cached at data/raw/lineups.parquet.

    HOW TO TEST
        df = fetch_lineups()
        df[df.team == "Manchester United"].formation.value_counts()

    EXPECTED RESULT
        every United match has a formation string like "4-2-3-1"; the counts add up to the number of
        matches played; the most common formation(s) match what you remember watching. If lineups
        are missing for many matches, say so and fall back to inferring shape from minutes/positions.
    """
    raise NotImplementedError


def fetch_market_data() -> pd.DataFrame:
    """Market value and contract expiry per player.

    GOAL     Needed for the contract filter (config: contract_expiry_cutoff_months) and price sanity checks.
    OUTPUT   player, club, market_value_eur, contract_expiry (date); cached under data/raw/.

    HOW TO TEST
        df = fetch_market_data(); df.isna().mean()

    EXPECTED RESULT
        a row for most players with 450+ minutes; market_value_eur and contract_expiry mostly present
        (<15% NA); values plausible (stars in tens of millions, not zeros). Optional - skip it until the
        footballing-fit part works.
    """
    raise NotImplementedError
