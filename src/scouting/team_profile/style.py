"""MODULE 3a - TEAM STYLE: "How does Manchester United play, and who plays similarly?"

WHY THIS MODULE EXISTS
    The project premise is that a signing must fit the SYSTEM. This module turns each team's season
    into a vector of style numbers (possession, pressing, directness, width, shot volume/quality ...),
    groups the ~96 teams per season into style families, and shows where United sits and which teams
    are its closest peers. Modules 4-5 use those peers as the benchmark.

INPUT    team tables (data/raw/fbref_team_*.parquet now; add Understat PPDA/xG and lineups for better
         features - see data/sources.py). There are 96 team-seasons per season, 192 in total.
OUTPUT   style matrix (one row per team-season), cluster labels, and a TeamStyle profile for United.

FUNCTION ORDER   build_style_matrix -> fit_style_clusters -> describe_team  (infer_formation_usage separate)

HOW TO RUN / TEST   notebook with %autoreload 2 and plots (this module is judged mostly by looking at
    results); `pytest -q tests/test_acceptance.py -k style_matrix` for the structural check.

WHAT "GOOD" LOOKS LIKE   the clusters and peer lists should make football sense to you. If Manchester
    City and a relegation side share a cluster, a feature is wrong or the scaling is off.
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
    """Build one standardised feature row per team-season.

    GOAL     numbers that describe HOW a team plays. With the current FBref data you can already build:
             possession (Poss), shots per 90, shot accuracy, crosses per 90, fouls per 90, tackles+interceptions
             per 90, cards per 90, goals per 90. (Better: xG, xGA, PPDA once Understat is added.)
    INPUT    {"standard": df, "shooting": df, "misc": df, ...} team tables; normalise counts to per-90 first
    OUTPUT   DataFrame indexed by (team, season), one column per feature, each column z-scored
             (mean 0, standard deviation 1) so no feature dominates by scale.

    HOW TO TEST
        m = build_style_matrix({"standard": read_raw("team_standard"), "shooting": read_raw("team_shooting"),
                                "misc": read_raw("team_misc")})
        m.shape; m.mean().round(6).abs().max(); m.std().round(3).unique(); m.isna().sum().sum()
        m.loc[("Manchester Utd", "2526")].sort_values()   # United's most extreme features
        pytest -q tests/test_acceptance.py -k style_matrix

    EXPECTED RESULT
        about 192 rows (96 per season; promoted/relegated clubs make ~110 distinct teams),
        0 duplicated index values, no NA, every column mean ~0 and std ~1.
        Sanity check: the teams with the highest possession z-score should be the ones you expect
        (Bayern, Barcelona, Man City ...); if they are not, a column is mis-scaled or mis-joined.
    """
    raise NotImplementedError


def fit_style_clusters(style_matrix: pd.DataFrame, k_range: range = range(3, 9)):
    """Group teams into style families and justify the number of groups.

    GOAL     try k = 3..8 clusters (KMeans, then a Gaussian Mixture for soft membership), score each k
             (silhouette score, BIC for GMM), pick one and WRITE DOWN why. Optionally reduce with PCA first.
    OUTPUT   (fitted_model, labels) - labels is a Series indexed like style_matrix.

    HOW TO TEST
        model, labels = fit_style_clusters(m)
        labels.value_counts()
        # plot silhouette vs k; 2D scatter (PCA or UMAP) coloured by cluster, labelled with team names
        # stability: refit on a bootstrap sample 20 times, check teams stay with the same peers (Adjusted Rand index)

    EXPECTED RESULT
        a silhouette score clearly above 0 (above ~0.2 is decent for real football data; do not expect 0.7);
        no cluster with fewer than ~5 teams; the scatter shows some structure; names in each cluster
        read as a coherent family (e.g. possession-dominant top sides vs low-block counter-attackers).
        Different random seeds give mostly the same groups. Honest finding "clusters are fuzzy" is OK -
        then lean on nearest-neighbour peers instead.
    """
    raise NotImplementedError


def describe_team(team: str, season: str, style_matrix: pd.DataFrame, model) -> TeamStyle:
    """Profile of the target club: where it sits and who its peers are.

    GOAL     answer in plain terms: "United are a X-style team; their closest peers are A, B, C;
             they are extreme on features P and Q."
    INPUT    team="Manchester Utd", season="2627"
    OUTPUT   TeamStyle (nearest_peers = config team_profile.n_peer_teams closest teams by Euclidean/cosine
             distance, excluding the team itself and, ideally, other seasons of the same team).

    HOW TO TEST
        s = describe_team("Manchester Utd", "2627", m, model)
        s.cluster, s.nearest_peers, s.vector.sort_values().head(3), s.vector.sort_values().tail(3)

    EXPECTED RESULT
        8 peers, none equal to Manchester Utd; peers come from several leagues; the most extreme
        features match what you know about United's current play (if the data says "highest crossing
        rate in Europe" and that is wrong, investigate the data, not the team).
    """
    raise NotImplementedError


def infer_formation_usage(lineups: pd.DataFrame, team: str) -> pd.Series:
    """How often United use each formation (recency-weighted).

    GOAL     answer "which system?" with numbers. Needs data/sources.fetch_lineups().
    OUTPUT   Series: formation -> share (sums to 1). Weight recent matches more (config time_decay_factor).

    HOW TO TEST
        infer_formation_usage(fetch_lineups(), "Manchester United")

    EXPECTED RESULT   e.g. {"4-2-3-1": 0.55, "3-4-2-1": 0.30, "4-4-2": 0.15} - values sum to 1.0 and
                      match what you remember watching. Share must be computed on matches, not on lineups rows.
    """
    raise NotImplementedError
