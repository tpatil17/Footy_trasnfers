"""Module 5b - Player similarity + system fit.

Two questions:
  * "Who plays like X?" (replace a departing/ageing player) -> nearest neighbours in feature/embedding space
  * "Who suits OUR system?" -> distance between a candidate's profile and the profile of the ideal player
    for United's style at that role (e.g. the role slot's centroid among teams in United's style cluster)

Progression ladder (do them in order and compare!):
  1. cosine similarity on standardised percentiles
  2. PCA-whitened + Mahalanobis distance
  3. learned embedding (autoencoder in PyTorch, or contrastive learning using the same player across seasons as positives)
Evaluate: do the nearest neighbours of well-known players look right? Is a player's season-1 vector closest
to their own season-2 vector (self-retrieval accuracy)?
"""
from __future__ import annotations

import pandas as pd


def similar_players(player: str, season: str, pool: pd.DataFrame, k: int = 10) -> pd.DataFrame:
    raise NotImplementedError


def system_fit_score(candidates: pd.DataFrame, ideal_profile: pd.Series) -> pd.Series:
    """0-1 score of how well each candidate matches the ideal profile for the target role/system."""
    raise NotImplementedError


def build_ideal_profile(role: str, style_cluster_teams: list[str], player_table: pd.DataFrame) -> pd.Series:
    """Profile of the typical high-minute player in `role` at teams that play like the target club."""
    raise NotImplementedError
