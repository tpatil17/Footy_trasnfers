"""Module 5a - Role discovery: FBref's GK/DF/MF/FW is far too coarse.

Cluster players *within* a position group on role-relevant features to discover archetypes
(ball-playing CB vs stopper, destroyer vs deep playmaker, inside forward vs target man...).

ML you practise: feature selection per position, PCA/NMF, GMM soft roles ("70% box-to-box, 30% DM"),
cluster validation, naming clusters by inspecting centroids (human-in-the-loop).
"""
from __future__ import annotations

import pandas as pd


def fit_role_model(player_table: pd.DataFrame, position_group: str):
    """Fit a role clustering model for one position group. Persist with joblib under data/processed/models/."""
    raise NotImplementedError


def assign_roles(player_table: pd.DataFrame) -> pd.DataFrame:
    """Adds `role` and `role_probs` columns."""
    raise NotImplementedError
