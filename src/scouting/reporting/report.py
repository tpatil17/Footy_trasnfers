"""MODULE 9 - REPORTING: the final deliverable.

WHY THIS MODULE EXISTS
    The goal of the project is a list: player | position | why that position needs filling | why this player.
    This module writes it to a file you can read and share.

OUTPUT FILES (data/processed/)
    shortlist_manchester_united_<window>.csv
    shortlist_manchester_united_<window>.md   (readable report)

HOW TO RUN / TEST
    recs = top_targets(...)   # or run_agent(...)
    to_dataframe(recs); write_markdown_report(recs, "data/processed/shortlist.md")
"""
from __future__ import annotations

from scouting.scoring.ranker import Recommendation


def to_dataframe(recs: list[Recommendation]) -> "pd.DataFrame":  # noqa: F821
    """GOAL     one row per recommendation with the columns: player, club, age, position (role), need_role,
             score, why_position_needed, why_player_fits.
    HOW TO TEST
        df = to_dataframe(recs); df.shape; df.columns.tolist(); df.isna().sum()
    EXPECTED RESULT
        len(recs) rows, the 8 columns above, zero NA in the two explanation columns, sorted by need then score.
    """
    raise NotImplementedError


def write_markdown_report(recs: list[Recommendation], path: str) -> None:
    """GOAL     a readable report: a short intro (club style + top needs), then one section per need with a table
             of targets and 1-2 sentences per player.
    HOW TO TEST
        write_markdown_report(recs, "data/processed/shortlist.md")  then open the file.
    EXPECTED RESULT
        the file opens in a Markdown viewer; sections in need order; every target shows position, club, age
        and both explanations. Someone who has never seen the code understands why each player is listed.
        Stretch: percentile radar chart (mplsoccer) per target vs the current starter.
    """
    raise NotImplementedError
