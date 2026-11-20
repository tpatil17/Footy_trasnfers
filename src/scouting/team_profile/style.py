"""Module 3a - "What system does this team play?"  (unsupervised learning)

Build a style vector per (team, season) -> reduce dimensions -> cluster -> locate Manchester United.

Style axes you will want (need richer data than FBref gives, see data/sources.py):
  possession share, PPDA / pressing intensity, directness, width (crosses), shot volume vs shot quality,
  chance-creation sources, defensive line height proxy, set-piece reliance, formation(s) used.

ML you practise: standardisation, PCA, KMeans vs Gaussian Mixture (soft membership), silhouette /
BIC for choosing k, UMAP/t-SNE for visualisation, cluster stability (bootstrap).
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class TeamStyle:
    team: str
    season: str
    vector: pd.Series           # standardised style features
    cluster: int
    cluster_probs: pd.Series    # soft membership if using a GMM
    nearest_peers: list[str]    # most similar teams by style


def build_style_matrix(team_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per (team, season), columns = style features, standardised."""
    raise NotImplementedError


def fit_style_clusters(style_matrix: pd.DataFrame, k_range: range = range(3, 9)):
    """Choose k with silhouette/BIC, return the fitted model + labels. Log how you decided on k."""
    raise NotImplementedError


def describe_team(team: str, season: str, style_matrix: pd.DataFrame, model) -> TeamStyle:
    """Profile for the target club: where it sits, which peers are closest, which axes are extreme."""
    raise NotImplementedError


def infer_formation_usage(lineups: pd.DataFrame, team: str) -> pd.Series:
    """Share of minutes per formation (and per role slot), recency-weighted."""
    raise NotImplementedError
