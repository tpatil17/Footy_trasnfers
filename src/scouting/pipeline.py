"""End-to-end orchestration. Each stage should be re-runnable and cache its output under data/interim|processed.

    python -m scouting.pipeline            # run all stages
    python -m scouting.pipeline --stage needs
"""
from __future__ import annotations

import argparse

STAGES = ["ingest", "clean", "features", "team_profile", "needs", "roles", "score", "agent", "report"]


def run(stage: str | None = None) -> None:
    """TODO: wire stages together as you finish each module. Start by just running `ingest` + `clean`."""
    raise NotImplementedError


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=STAGES, default=None)
    run(ap.parse_args().stage)
