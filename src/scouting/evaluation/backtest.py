"""MODULE 8 - EVALUATION: how do you know the system is any good?

WHY THIS MODULE EXISTS
    A pipeline that outputs plausible names is easy to build and easy to fool yourself with. This module
    gives you evidence: does the method beat simple alternatives, is it stable, and does the LLM stick
    to the facts? It is the module that turns a hobby project into something you can defend.

DO THIS AFTER   a first end-to-end shortlist exists (Modules 1-6). Needs history: you only have two seasons
    now, so a real backtest requires fetching earlier seasons (add them to config.yaml and re-run ingestion).

FOUR CHECKS
    1. Backtest   pretend it is an earlier window, use ONLY data from before it, see how your picks did.
    2. Ablations  remove one ingredient at a time (system fit, shrinkage, roles) - which ones help?
    3. Stability  do needs/targets survive small changes (drop a season, resample)?
    4. Grounding  are the numbers quoted in the LLM text real?

HOW TO RUN / TEST   notebook; each function states what a good outcome is. Honest "this did not help"
    results are valuable - record them in docs/ROADMAP.md.
"""
from __future__ import annotations


def backtest_window(season_cutoff: str) -> dict:
    """Replay a past transfer window.

    GOAL     with data up to `season_cutoff` only (e.g. "2425"), produce a shortlist for that club, then compare to
             what happened: (a) did actual signings or well-regarded targets rank high on your list, and
             (b) did players you ranked high improve or hold their level the next season (compare their
             quality percentile in the following season).
    LEAKAGE  never use any row dated after the cutoff - split by time, not randomly.
    OUTPUT   {"hit_rate_top25": ..., "mean_next_season_change_top": ..., "mean_next_season_change_baseline": ...}
    HOW TO TEST
        backtest_window("2425")
    EXPECTED RESULT
        your top picks' average next-season change in quality percentile is >= the average of a baseline that
        simply picks the highest-quality players (i.e. system fit and age add something), or you learn
        they do not. With only a few windows the result is noisy - report that, do not over-claim.
    """
    raise NotImplementedError


def ablation_report(variants: dict) -> "pd.DataFrame":  # noqa: F821
    """Compare pipeline variants side by side.

    GOAL     variants = {"full": pipeline_fn, "no_system_fit": ..., "no_shrinkage": ..., "no_roles": ...};
             run each on the same backtest and tabulate the metrics.
    OUTPUT   DataFrame: variant x metric.
    HOW TO TEST   ablation_report({...}) with at least 3 variants.
    EXPECTED RESULT
        a table in which the full pipeline is usually (not necessarily always) best; any component that does
        not help is a candidate for removal. Differences smaller than the run-to-run noise are not findings.
    """
    raise NotImplementedError


def grounding_check(rationale: str, tool_outputs: list[dict]) -> float:
    """Check whether the numbers in an LLM explanation are real.

    GOAL     extract every number from `rationale` (regex), and count how many appear (allowing rounding)
             in the JSON of `tool_outputs`.
    OUTPUT   fraction between 0 and 1.
    HOW TO TEST (write these as unit tests)
        grounding_check("Cunha has 0.42 xG per 90.", [{"xg_p90": 0.42}])           # -> 1.0
        grounding_check("Cunha has 0.90 xG per 90.", [{"xg_p90": 0.42}])           # -> 0.0
        grounding_check("No numbers here.", [])                                      # -> 1.0 (nothing to verify)
    EXPECTED RESULT
        the three results above; across real agent runs a score >= 0.95; any number that fails is a
        hallucination you can inspect.
    """
    raise NotImplementedError
