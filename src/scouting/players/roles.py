"""MODULE 5a - ROLES: discover what KIND of defender/midfielder/forward each player is.

WHY THIS MODULE EXISTS
    FBref only says GK/DF/MF/FW. "A midfielder" could be a destroyer, a deep playmaker or a box-to-box
    runner, and United may need exactly one of those. This module discovers the sub-types from the data
    so needs can be stated as "a ball-winning DM", not just "a midfielder".

METHOD   within each position group, cluster players on role-relevant features (from Module 2),
         look at what each cluster's average player does, and NAME the clusters yourself.

INPUT    player features (Module 2) with percentile columns, filtered to players with enough minutes
OUTPUT   `role` (best cluster name) and `role_probs` (soft membership) columns on the player table.

HOW TO RUN / TEST   notebook. Roles are judged by whether they make football sense, so print the
    top-10 players of every cluster and check you recognise the archetype.
"""
from __future__ import annotations

import pandas as pd


def fit_role_model(player_table: pd.DataFrame, position_group: str):
    """Cluster one position group into roles.

    GOAL     for position_group in GK/DF/MF/FW: pick role-relevant features (e.g. for MF: tackles, interceptions,
             crosses, shots, goals, assists, fouls per 90), standardise, optionally PCA, fit a Gaussian Mixture
             with k = 3-5, choose k with BIC/silhouette.
    OUTPUT   fitted model (also saved with joblib to data/processed/models/roles_<group>.joblib)

    HOW TO TEST
        model = fit_role_model(features, "MF")
        labels = model.predict(X)    # X = the same feature matrix
        for c in sorted(set(labels)):
            print(c, features[labels == c].sort_values("minutes").tail(10)[["player", "team"]])

    EXPECTED RESULT
        3-5 clusters per group, each with at least ~5% of players; cluster centroids that differ on
        interpretable features; the top players in each cluster agree with the name you give it
        (you should be able to say "this cluster is the destroyers"). If clusters are only separated by
        minutes played, your features are not normalised properly.
    """
    raise NotImplementedError


def assign_roles(player_table: pd.DataFrame) -> pd.DataFrame:
    """Label every player with a role.

    GOAL     use the fitted models to add `role` (a name you chose) and `role_probs` (e.g. {"DM": 0.7, "CM": 0.3}).
    OUTPUT   player table plus those two columns; GKs get role "GK".

    HOW TO TEST
        out = assign_roles(features)
        out.groupby(["pos_primary", "role"]).size()
        out[out.player == "Bruno Fernandes"][["player", "role", "role_probs"]]   # any player you know well

    EXPECTED RESULT
        every row has a role; role counts per position look sensible (no role with 3 players or 90% of the
        group); well-known players land in the role you would expect; the probabilities sum to 1.
    """
    raise NotImplementedError
