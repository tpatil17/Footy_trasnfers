"""Module 9 - Final deliverable: the shortlist (player | position | why that position needs filling | why him).

Output: data/processed/shortlist_<club>_<window>.csv + a readable markdown report.
Stretch: radar/percentile charts per target vs the incumbent (mplsoccer) and a small Streamlit app.
"""
from __future__ import annotations

from scouting.scoring.ranker import Recommendation


def to_dataframe(recs: list[Recommendation]) -> "pd.DataFrame":  # noqa: F821
    raise NotImplementedError


def write_markdown_report(recs: list[Recommendation], path: str) -> None:
    raise NotImplementedError
