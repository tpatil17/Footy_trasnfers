"""MODULE 1c - IDENTITY: match the same player/team across different data sources.

WHY THIS MODULE EXISTS
    Once you add Understat/ESPN/Transfermarkt data, every source spells names differently:
    "Manchester Utd" (FBref) vs "Manchester United" (Understat), "Bruno Fernandes" vs
    "Bruno Miguel Borges Fernandes", accents, hyphens. Without matching, joins silently lose players.

DO THIS AFTER   at least one extra source in data/sources.py is working.

FUNCTION ORDER   normalise_name -> match_teams (small, do by hand) -> match_players (the real work)

HOW TO RUN / TEST   toy examples first (each function below lists them), then run on real tables and
    READ the unmatched list. Never trust a match rate without looking at examples.
"""
from __future__ import annotations

import pandas as pd


def normalise_name(name: str) -> str:
    """Make names comparable: lowercase, no accents, no punctuation, single spaces.

    GOAL     two spellings of one name should become the same string.
    HOW TO TEST
        normalise_name("  Christian  Nørgaard ")
        normalise_name("N'Golo Kanté")
        normalise_name("Kylian Mbappé-Lottin")
    EXPECTED RESULT
        "christian norgaard", "ngolo kante", "kylian mbappe lottin"
        (tip: unidecode is already installed; "ø" must become "o").
    """
    raise NotImplementedError


def match_players(left: pd.DataFrame, right: pd.DataFrame, threshold: float = 90.0) -> pd.DataFrame:
    """Match players between two sources.

    GOAL     for each row in `left` (e.g. FBref), find the same player in `right` (e.g. Understat).
    METHOD   1) block: only compare players with the same birth year and nationality
             2) within a block, fuzzy-match normalised names (rapidfuzz.fuzz.WRatio, 0-100)
             3) accept the best match only if its score >= threshold
    OUTPUT   left plus `right_id` and `match_score` (NA when no match above the threshold).

    HOW TO TEST
        out = match_players(fbref_players_2526, understat_players_2526)
        out.match_score.notna().mean()
        out.sort_values("match_score").dropna().head(30)   # READ these 30 lowest accepted matches
        out[out.match_score.isna()].sort_values("Playing Time_Min", ascending=False).head(20)  # who got missed?

    EXPECTED RESULT
        match rate >= 95% among players with 450+ minutes. The 30 weakest accepted matches should look
        right to a human (same person). The unmatched high-minute players should be explainable
        (nickname, different spelling) - then add them to a manual override file. Wrong matches are worse
        than missing ones, so raise the threshold if you see mistakes.
    """
    raise NotImplementedError


def match_teams(left: pd.Series, right: pd.Series) -> dict[str, str]:
    """Build a team-name mapping between two sources.

    GOAL     only ~96 clubs, so fuzzy-match to propose a mapping and then FIX IT BY HAND; save it to
             config/team_map.yaml so it is reproducible.
    HOW TO TEST
        m = match_teams(fbref_teams, understat_teams)
        m["Manchester Utd"]
        assert set(m) == set(fbref_teams)
    EXPECTED RESULT
        m["Manchester Utd"] == "Manchester United"; every FBref team has exactly one partner;
        no two FBref teams map to the same partner (check for e.g. Manchester City/United mix-ups).
    """
    raise NotImplementedError
