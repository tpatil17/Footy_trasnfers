"""Module 1c - Entity resolution: the same player/team has different names in every source.

"Manchester Utd" (FBref) vs "Manchester United" (Understat/ESPN) vs "Man United" (Transfermarkt);
"Bruno Fernandes" vs "Bruno Miguel Borges Fernandes"; accents; hyphens.

Learning goal: fuzzy matching + blocking (rapidfuzz / record-linkage ideas), precision vs recall of the
match, and a human-reviewable "unmatched" report instead of silently dropping rows.
"""
from __future__ import annotations

import pandas as pd


def normalise_name(name: str) -> str:
    """lowercase, strip accents (unidecode), drop punctuation, collapse whitespace."""
    raise NotImplementedError


def match_players(left: pd.DataFrame, right: pd.DataFrame, threshold: float = 90.0) -> pd.DataFrame:
    """Return left rows with `right_id` + `match_score`. Block on (born year, nation) first, then fuzzy-match names.

    Done when: you can report match rate, and manually inspect the 30 lowest-score accepted matches.
    """
    raise NotImplementedError


def match_teams(left: pd.Series, right: pd.Series) -> dict[str, str]:
    """Small enough (~96 clubs) to build a mapping dict + review by hand; persist it as config/team_map.yaml."""
    raise NotImplementedError
