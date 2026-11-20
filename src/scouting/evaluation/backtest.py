"""Module 8 - How do you know the system is any good?  (the module most hobby projects skip)

 1. Backtest the recommender: pretend it is a past window (e.g. summer 2024), use only data available
    then, and check whether real signings/top targets score highly and whether recommended players
    improved the next season (age-curve-adjusted). Avoid look-ahead leakage - split by time, never random.
 2. Ablations: does system-fit beat raw quality ranking? does shrinkage help? do roles help?
 3. Stability: do the needs/targets change wildly under small perturbations (bootstrap, drop a season)?
 4. LLM output evaluation: factual grounding (every number in the rationale appears in tool output),
    consistency across runs, an LLM-as-judge rubric checked against your own judgement on ~20 samples.
 5. Sanity cases: known facts (e.g. a team that obviously lacks a striker should show that need).
"""
from __future__ import annotations


def backtest_window(season_cutoff: str) -> dict:
    raise NotImplementedError


def ablation_report(variants: dict) -> "pd.DataFrame":  # noqa: F821
    raise NotImplementedError


def grounding_check(rationale: str, tool_outputs: list[dict]) -> float:
    """Fraction of numeric claims in `rationale` that can be traced to `tool_outputs`."""
    raise NotImplementedError
