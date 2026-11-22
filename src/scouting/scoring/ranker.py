"""MODULE 6 - SCORING: turn "United need a DM" into a ranked list of named players.

WHY THIS MODULE EXISTS
    Modules 4-5 tell you WHAT is needed and what a fitting player looks like. This module searches all Big-5
    players, removes impossible targets, scores the rest, and returns the top few per need.

SCORE (start simple and keep this as the baseline forever)
    score = 0.35*quality + 0.30*system_fit + 0.20*upgrade_over_incumbent + 0.15*age_trajectory
    (weights are in config.yaml -> scoring.weights; all four parts are scaled to 0-1)
      quality                   percentile within position/role (Module 2)
      system_fit                Module 5 system_fit_score
      upgrade_over_incumbent    how much better than United's current starter in that role
      age_trajectory            expected change next season given age (age curve; simple rule first)

FUNCTION ORDER   apply_hard_filters -> expected_next_season -> score_candidates -> top_targets
THEN (stretch)   replace the hand weights with learned ones (learning-to-rank) and compare to the baseline.

HOW TO RUN / TEST   notebook with real data; `pytest -q tests/test_acceptance.py -k recommendations` for the
    output contract. Judge the shortlist by reading it: would a scout laugh at any name?
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
    """Remove players who cannot be realistic targets.

    GOAL     keep a candidate only if: age within config preprocessing.age_range (18-29), enough minutes
             (Module 2 minutes_filter), not already at Manchester United, and (if market data exists)
             contract not far beyond the cutoff.
    HOW TO TEST
        out = apply_hard_filters(all_players)
        len(all_players), len(out)
        out.age.min(), out.age.max(), (out.team == "Manchester Utd").sum()
    EXPECTED RESULT
        a clear drop in size (roughly 2000 of ~5000 player-seasons survive the minutes+age rule alone - see
        Module 2); all ages inside [18, 29]; zero United players.
    """
    raise NotImplementedError


def expected_next_season(candidates: pd.DataFrame) -> pd.DataFrame:
    """Predict next season's level from age.

    GOAL     young players are still improving, players near 30 decline. Start with a simple rule:
             a small bonus below 24, neutral 24-28, a penalty from 29. Later: fit an age curve from
             your data (players' change in per-90 stats between 2526 and 2627 by age, e.g. statsmodels).
    OUTPUT   candidates plus `age_trajectory` in [0, 1] (or an expected change in the quality percentile).
    HOW TO TEST
        out = expected_next_season(candidates)
        out.groupby(out.age.round()).age_trajectory.mean()
    EXPECTED RESULT
        trajectory falls with age after the mid-20s; a 21-year-old gets a higher value than a 29-year-old
        at the same current level; no NA.
    """
    raise NotImplementedError


def score_candidates(candidates: pd.DataFrame, need, incumbent: pd.Series, weights: dict[str, float]) -> pd.DataFrame:
    """Score candidates for ONE need.

    GOAL     compute the four components, combine with `weights`, keep the components as columns so the
             explanation can quote them.
    INPUT    candidates filtered to the need's role, the PositionNeed, the incumbent's feature vector, weights
    OUTPUT   candidates plus quality, system_fit, upgrade, age_trajectory, score; sorted by score descending.
    HOW TO TEST
        ranked = score_candidates(cands, need, incumbent, cfg["scoring"]["weights"])
        ranked.head(10)[["player", "team", "age", "quality", "system_fit", "upgrade", "score"]]
        # set one weight to 1 and others to 0: the ranking must equal the ranking by that component
    EXPECTED RESULT
        score in [0, 1]; weights sum to 1; the head of the list contains plausible, well-known
        high performers for the role; the weight-isolation check passes exactly.
    """
    raise NotImplementedError


def top_targets(needs: list, player_table: pd.DataFrame, n_per_need: int = 5) -> list[Recommendation]:
    """The final shortlist.

    GOAL     for each of the top needs (Module 4): filter, score, take n_per_need best, and fill every field of
             Recommendation - including `why_position_needed` (from the need's reasons) and `why_player_fits`
             (built from the strongest components of his score).
    HOW TO TEST
        recs = top_targets(needs, features)
        pd.DataFrame([r.__dict__ for r in recs])
        pytest -q tests/test_acceptance.py -k recommendations
    EXPECTED RESULT
        up to 5 needs x 5 players = 25 rows; no player twice; every row has a non-empty
        why_position_needed and why_player_fits that quote numbers; mix of leagues and clubs;
        read the list as a scout: most names make sense, a few surprises are worth a closer look.
    """
    raise NotImplementedError
