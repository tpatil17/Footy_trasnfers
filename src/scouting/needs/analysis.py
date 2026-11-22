"""MODULE 4 - NEEDS: "Where does Manchester United need to improve, and why?"

WHY THIS MODULE EXISTS
    This is the analytical heart of the project and the part the final list must explain
    ("why that position needs to be filled"). It turns the clean player data and the team style
    profile into a ranked list of positions with numeric evidence and plain-English reasons.

THREE LENSES (each gives a score per position; the final ranking combines them)
    1. BENCHMARK GAP   how does United's output at that position compare with similar teams (the peers
                       from Module 3) and with the teams above them in the table?
    2. SQUAD STRUCTURE is the starter old, is there no depth behind him, does one player play 90% of
                       the minutes, does his contract expire?
    3. IMPACT MODEL    which positions' quality best explains team results across all 96 team-seasons?
                       (a position that matters more for winning deserves more weight)

INPUT    data/processed/player_features.parquet (Module 2), style peers (Module 3)
OUTPUT   list[PositionNeed], sorted most urgent first. Each carries `severity`, `evidence`, `reasons`.

FUNCTION ORDER   benchmark_gaps, squad_structure_risks, fit_impact_model (independent) -> rank_needs

HOW TO RUN / TEST   notebook for looking; `pytest -q tests/test_acceptance.py -k needs` for the contract.

THE REAL TEST   do the top needs agree with what you, as a United fan, can see and defend? If the model
    says "United's biggest need is goalkeeper" and their keeper is excellent, find out why before
    trusting anything. Only 96 team-seasons exist per season, so expect noisy estimates - report ranges.
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
    """Compare United's output at each position with the peer teams'.

    GOAL     For every position (start with GK/DF/MF/FW, later tactical roles) compute United's
             minutes-weighted average of key stats and express the difference to the peer average as a
             z-score. Negative = United worse than peers.
    INPUT    team="Manchester Utd", season, the player feature table, peers=list of team names
    OUTPUT   DataFrame: one row per position, one column per metric, values are z-scores.

    HOW TO TEST
        gaps = benchmark_gaps("Manchester Utd", "2627", features, peers)
        gaps.round(2)
        # sanity: benchmark_gaps(peer_team, ..., peers=[all other peers]) should average ~0 across teams
        # sanity: compare a team with itself -> all zeros

    EXPECTED RESULT
        a small table (4 rows for coarse positions); most z-scores between -2 and +2; some negatives
        and some positives (a team is not worse at everything). Forwards should show goal/shot metrics,
        defenders tackle/interception metrics. Different peer lists give broadly the same sign.
    """
    raise NotImplementedError


def squad_structure_risks(team: str, season: str, player_table: pd.DataFrame) -> pd.DataFrame:
    """Find positions that are structurally fragile.

    GOAL     Flag positions where: the main starter is 30+; minutes are concentrated (top player has
             > 70% of the position's minutes = no depth); few players have > 450 minutes; contracts expire
             within `contract_expiry_cutoff_months` (needs market data, skip at first).
    OUTPUT   DataFrame: one row per position with columns avg_starter_age, minutes_share_top1, n_regulars,
             risk_score (0-1).

    HOW TO TEST
        risks = squad_structure_risks("Manchester Utd", "2627", features)
        risks.sort_values("risk_score", ascending=False)

    EXPECTED RESULT
        one row per position; a position with a 33-year-old starter and no 450-minute backup scores
        near the top; risk_score always in [0, 1]. Eyeball the squad list yourself - the numbers should
        agree with what you see.
    """
    raise NotImplementedError


def fit_impact_model(team_season_table: pd.DataFrame, target: str = "goal_diff_p90"):
    """Learn which positions' quality explains results.

    GOAL     Regress goal difference per 90 (or points per match) on position-group quality (e.g. average
             forward quality, midfield quality, defender quality, keeper quality) across team-seasons.
             With ~96 rows use regularisation (Ridge/ElasticNet) and cross-validation grouped by team
             (a team's two seasons must not be split across train and test).
    OUTPUT   (model, importances) - importances = coefficient/SHAP value per position group, with
             bootstrap confidence intervals.

    HOW TO TEST
        model, imp = fit_impact_model(team_table)
        imp
        # cross-validated R^2 (grouped by team); compare with a baseline that predicts the mean

    EXPECTED RESULT
        CV R^2 above 0 (even 0.2-0.5 is a good result with this little data - if you get 0.95 you
        have leakage, e.g. a feature that contains goals); importances with wide error bars; the
        direction is sensible (better attack/defence quality -> better goal difference). If importances are
        all ~0, say so: the position weighting then falls back to equal weights.
    """
    raise NotImplementedError


def rank_needs(team: str, season: str, **inputs) -> list[PositionNeed]:
    """Combine the three lenses into the final ranked list of needs.

    GOAL     severity = weighted sum of the three lenses (weights live in config.yaml -> needs.lens_weights:
             benchmark_gap 0.4, squad_structure 0.3, impact_model 0.3). Each PositionNeed must have `reasons`,
             written like: "Forwards create 1.1 SD fewer shots per 90 than similar teams, and the starting
             striker is 33 with no 450-minute backup."
    OUTPUT   list[PositionNeed] sorted by severity, length = config needs.top_n_needs (5).

    HOW TO TEST
        needs = rank_needs("Manchester Utd", "2627", ...)
        for n in needs: print(n.role, round(n.severity, 2), n.reasons)
        pytest -q tests/test_acceptance.py -k needs_are_ranked
        # change the lens weights and see which needs move - robust needs stay in the top 5

    EXPECTED RESULT
        5 needs, severity descending, in [0, 1]; each with at least one reason that quotes a number from the
        evidence dict; top needs that a knowledgeable fan would agree with; the top 2-3 do not change when
        you perturb the lens weights by +/-0.1.
    """
    raise NotImplementedError
