"""Module 4 - Where does the team need to improve?  (the analytical heart of the project)

Three complementary lenses; the final need ranking should combine them and say WHY.

 1. Benchmark gap     - position-group output vs peers (similar-style teams AND the teams above you).
 2. Squad structure   - age profile, minutes concentration (one player = 90% of minutes at a position),
                        contract expiry, injury/availability, depth behind the starter.
 3. Impact model      - which position groups explain the gap in results? e.g. regress goal difference
                        or points on position-group quality across all 96 team-seasons (Ridge / GBM + SHAP),
                        and use `Team Success_On-Off` from playing_time as a player-level sanity check.

Beware: only ~96 team-seasons per season -> overfitting. Use regularisation, cross-validation grouped by
team, report uncertainty (bootstrap CIs) instead of single point estimates.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class PositionNeed:
    role: str                      # e.g. "DM", "LB", "ST"
    severity: float                # 0-1 combined score
    evidence: dict[str, float] = field(default_factory=dict)   # metric -> gap vs benchmark
    reasons: list[str] = field(default_factory=list)           # human-readable, used by the agent/report


def benchmark_gaps(team: str, season: str, player_table: pd.DataFrame, peers: list[str]) -> pd.DataFrame:
    """Per role: team's minutes-weighted quality vs the peer mean (z-score). Returns role x metric gaps."""
    raise NotImplementedError


def squad_structure_risks(team: str, season: str, player_table: pd.DataFrame) -> pd.DataFrame:
    """Per role: aging starters, thin depth, expiring contracts."""
    raise NotImplementedError


def fit_impact_model(team_season_table: pd.DataFrame, target: str = "goal_diff_p90"):
    """Regularised model of results ~ position-group quality. Return model + feature importances (SHAP/perm)."""
    raise NotImplementedError


def rank_needs(team: str, season: str, **inputs) -> list[PositionNeed]:
    """Combine the three lenses into a ranked list. Make the weighting explicit and configurable."""
    raise NotImplementedError
