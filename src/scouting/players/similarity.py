"""MODULE 5b - SIMILARITY AND SYSTEM FIT: "who plays like X?" and "who suits United's system?"

WHY THIS MODULE EXISTS
    Once you know the need (Module 4), you need candidates who (a) are good and (b) fit how United play.
    This module scores every player on how close they are to an "ideal profile" for the role in United's
    style of play, and can also find replacements for a specific player.

BUILD IT IN THREE STEPS AND COMPARE THEM
    1. cosine similarity on standardised percentiles (simplest; this is your baseline)
    2. PCA-whitened + Mahalanobis distance (accounts for correlated stats)
    3. a learned embedding (autoencoder or contrastive model in PyTorch - stretch goal)

HOW TO RUN / TEST   notebook. Judge by examples: the neighbours of players you know well must look right.
    Add a numeric check: "self-retrieval" - is a player's 2526 profile closest to his own 2627 profile?
"""
from __future__ import annotations

import pandas as pd


def similar_players(player: str, season: str, pool: pd.DataFrame, k: int = 10) -> pd.DataFrame:
    """Find the k players with the most similar statistical profile.

    GOAL     "Who plays like Bruno Fernandes?" Compare within the same position group; exclude the
             player himself; return k rows ordered by similarity.
    OUTPUT   DataFrame: player, team, age, similarity (0-1), plus the key stats for comparison.

    HOW TO TEST
        similar_players("Bruno Fernandes", "2526", features, k=10)
        # pick 3 players you know well and judge the lists
        # self-retrieval: for each player with both seasons, rank his own 2627 row among all 2627 rows
        # by similarity to his 2526 row - his own row should be top-5 for most (>60%) players

    EXPECTED RESULT
        the target never appears in his own list; similarity decreasing down the list; neighbours that are the same
        kind of player (attacking midfielders for Bruno, not defenders); self-retrieval top-5 rate well above
        chance (chance = 5 / ~600 players per position group = under 1%).
    """
    raise NotImplementedError


def build_ideal_profile(role: str, style_cluster_teams: list[str], player_table: pd.DataFrame) -> pd.Series:
    """Define "the ideal player for this role in United's kind of system".

    GOAL     average profile of high-minute players in `role` at teams that play like United
             (the peer teams from Module 3), maybe weighted toward the best-performing peer teams.
    OUTPUT   Series indexed by feature name (percentiles, 0-1).

    HOW TO TEST
        ideal = build_ideal_profile("DM", peers, features)
        ideal.sort_values()
        # compare with the profile of United's current starter in that role (diff = what to improve)

    EXPECTED RESULT
        values in [0, 1]; a recognisable archetype (a DM profile with high tackles/interceptions);
        built from at least ~8 players (print how many); not identical to United's current player
        (otherwise there is nothing to improve).
    """
    raise NotImplementedError


def system_fit_score(candidates: pd.DataFrame, ideal_profile: pd.Series) -> pd.Series:
    """How well does each candidate match the ideal profile?

    GOAL     one number per candidate in [0, 1] (1 = identical to the ideal). Cosine or distance-based,
             your choice; document it.
    OUTPUT   Series indexed like candidates.

    HOW TO TEST
        s = system_fit_score(candidates, ideal)
        s.describe(); candidates.assign(fit=s).sort_values("fit").tail(10)[["player", "team", "fit"]]
        # sanity: the ideal profile scored against itself = 1.0; against its negative = close to 0

    EXPECTED RESULT
        all scores in [0, 1], not all bunched at 0.99 (spread across the range); the top-ranked candidates
        are players whose stats visibly resemble the ideal profile; the score is not just a proxy
        for "plays many minutes" - check the correlation with minutes (should be low).
    """
    raise NotImplementedError
