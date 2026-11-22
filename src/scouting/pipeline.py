"""PIPELINE: run all stages in order (do this LAST, as you finish each module).

The idea: every stage reads the previous stage's saved file and saves its own, so you can re-run just
one stage while developing.

    stage          reads                              writes                                   module
    ingest         (internet)                         data/raw/*.parquet                       src/data/scripts + data/sources.py
    clean          data/raw                           data/interim/player_season*.parquet      data/clean.py
    features       data/interim                       data/processed/player_features.parquet   features/engineering.py
    team_profile   data/raw (+understat)              data/processed/team_style.parquet        team_profile/
    needs          processed features + style         data/processed/needs.json                needs/analysis.py
    roles          processed features                 data/processed/player_roles.parquet      players/roles.py
    score          needs + roles + features           data/processed/shortlist.parquet         scoring/ranker.py
    agent          tools                              data/processed/agent_shortlist.json      agent/
    report         shortlist                          data/processed/shortlist.md/.csv         reporting/report.py

HOW TO USE
    python -m scouting.pipeline --stage clean      # one stage
    python -m scouting.pipeline                    # everything

HOW TO TEST
    Start by wiring only `ingest` and `clean`, run `--stage clean`, and check the files appear.
EXPECTED RESULT
    running a stage twice gives the same output (deterministic - set random seeds); a stage that cannot
    find its input file fails with a message naming the stage that must be run first.
"""
from __future__ import annotations

import argparse

STAGES = ["ingest", "clean", "features", "team_profile", "needs", "roles", "score", "agent", "report"]


def run(stage: str | None = None) -> None:
    """Run one stage, or all stages in order. Add each stage here as you finish its module."""
    raise NotImplementedError


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=STAGES, default=None)
    run(ap.parse_args().stage)
