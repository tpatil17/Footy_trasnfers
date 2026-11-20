"""Module 3b - Manager profiling (uses config.manager_profiling).

Idea: a manager's *tactical fingerprint* persists across clubs. Profile the current United manager
from up to `lookback_seasons` of matches, weighting recent seasons with `time_decay_factor` and
down-weighting national-team matches by `national_team_weight_discount`.

Needs: manager-tenure data (who managed which club in which match) - not in the repo yet.
Learning goal: time-decayed weighted averages, handling small samples, separating manager effect from
squad effect (hint: compare the same manager at two clubs, or a club before/after a manager change).
"""
from __future__ import annotations

import pandas as pd


def load_manager_tenures() -> pd.DataFrame:
    """manager, club, start, end, is_national_team. Source TBD (Transfermarkt / Wikipedia / ESPN)."""
    raise NotImplementedError


def manager_style_profile(manager: str, match_features: pd.DataFrame, tenures: pd.DataFrame) -> pd.Series:
    """Weighted style vector for one manager (same axes as team_profile.style)."""
    raise NotImplementedError
