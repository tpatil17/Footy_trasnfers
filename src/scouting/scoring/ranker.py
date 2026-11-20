"""Module 6 - Candidate scoring and ranking.

Start with a transparent weighted score, then try to *learn* the weights.

  score = f(quality_percentile, system_fit, upgrade_over_incumbent, age_trajectory, availability/price)

Hard filters first (config.preprocessing: age range, minutes, contract), then rank.

Ladder:
  1. hand-weighted linear score (explainable baseline - keep it, it is your benchmark)
  2. learn weights: pairwise / learning-to-rank (LightGBM LambdaRank or a logistic pairwise model) with
     "historical successful signings" as positives - requires multiple past windows of data
  3. age curves: fit expected performance change by age and position (mixed-effects / GAM) to predict next
     season rather than rank on last season
  4. uncertainty: bootstrap / Bayesian posterior so you can say "likely better, but only 70% sure"
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Recommendation:
    player: str
    club: str
    age: float
    role: str
    need_role: str
    score: float
    why_position_needed: str            # the explanation the final list must contain
    why_player_fits: str
    evidence: dict[str, float] = field(default_factory=dict)


def apply_hard_filters(candidates: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def expected_next_season(candidates: pd.DataFrame) -> pd.DataFrame:
    """Age-curve adjustment: predicted performance next season."""
    raise NotImplementedError


def score_candidates(candidates: pd.DataFrame, need, incumbent: pd.Series, weights: dict[str, float]) -> pd.DataFrame:
    raise NotImplementedError


def top_targets(needs: list, player_table: pd.DataFrame, n_per_need: int = 5) -> list[Recommendation]:
    raise NotImplementedError
