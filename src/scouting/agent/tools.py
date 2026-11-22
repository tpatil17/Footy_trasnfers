"""MODULE 7a - AGENT TOOLS: the functions the LLM is allowed to call.

WHY THIS MODULE EXISTS
    The agent (7b) must never invent statistics. Instead it calls these tools, which wrap your analytics
    (Modules 3-6) and return small, JSON-serialisable results. The LLM decides WHICH tool to call and how
    to explain the results; the numbers always come from your code.

BUILD AFTER   Modules 3-6 work (each tool is a thin wrapper over a function you already wrote).

DESIGN RULES
    * return plain dicts/lists (no DataFrames) and keep outputs short (10 rows, not 500)
    * the model only sees the tool NAME, DESCRIPTION and JSON SCHEMA - write them carefully in TOOL_SCHEMAS
    * on bad input return {"error": "..."} the model can recover from, never raise

HOW TO RUN / TEST   call each tool directly in a notebook BEFORE any LLM is involved:
        from scouting.agent import tools
        tools.get_positional_needs("Manchester Utd", "2627")
    then `json.dumps(result)` must work.
"""
from __future__ import annotations

TOOL_SCHEMAS: list[dict] = [
    # TODO: one entry per function below, in the Anthropic tool format:
    # {"name": "get_team_profile", "description": "...when to use it...",
    #  "input_schema": {"type": "object", "properties": {...}, "required": [...]}}
]


def get_team_profile(team: str, season: str) -> dict:
    """GOAL     style summary of a team (Module 3).
    OUTPUT   {"cluster": int, "peers": [...], "formations": {"4-2-3-1": 0.55, ...}, "extreme_features": {...}}
    HOW TO TEST   get_team_profile("Manchester Utd", "2627")
    EXPECTED RESULT   8 peer names, formation shares summing to 1, 3 highest and 3 lowest features; JSON-serialisable;
                      get_team_profile("Not A Team", "2627") returns {"error": ...}.
    """
    raise NotImplementedError


def get_positional_needs(team: str, season: str, top_n: int = 5) -> list[dict]:
    """GOAL     ranked needs (Module 4).
    OUTPUT   [{"role": "DM", "severity": 0.81, "evidence": {...}, "reasons": ["..."]}, ...]
    HOW TO TEST   get_positional_needs("Manchester Utd", "2627", top_n=3)
    EXPECTED RESULT   3 dicts, severity descending, each with reasons; identical output to calling rank_needs directly.
    """
    raise NotImplementedError


def search_candidates(role: str, max_age: int, min_minutes: int, leagues: list[str] | None = None, limit: int = 10) -> list[dict]:
    """GOAL     top candidates for a role with simple filters (Module 6).
    OUTPUT   up to `limit` dicts: player, club, age, minutes, score components.
    HOW TO TEST   search_candidates("DM", max_age=26, min_minutes=900, leagues=["ESP-La Liga"], limit=5)
    EXPECTED RESULT   at most 5 rows, all from La Liga, all aged <= 26 with >= 900 minutes, sorted by score.
    """
    raise NotImplementedError


def compare_players(player_a: str, player_b: str, season: str) -> dict:
    """GOAL     side-by-side comparison of two players' key percentiles.
    OUTPUT   {"player_a": {...}, "player_b": {...}, "biggest_differences": [...]}
    HOW TO TEST   compare_players("Bruno Fernandes", "Another Midfielder", "2526")
    EXPECTED RESULT   same metrics for both, percentiles in [0, 1], the biggest differences listed; unknown name -> {"error": ...}.
    """
    raise NotImplementedError


def similar_to(player: str, season: str, k: int = 5) -> list[dict]:
    """GOAL     wrapper over players.similarity.similar_players.
    HOW TO TEST   similar_to("Bruno Fernandes", "2526", k=5)
    EXPECTED RESULT   5 dicts, similarity descending, the player himself excluded.
    """
    raise NotImplementedError


def dispatch(tool_name: str, tool_input: dict):
    """GOAL     route a tool call from the model to the function above.
    HOW TO TEST   dispatch("get_positional_needs", {"team": "Manchester Utd", "season": "2627"})
    EXPECTED RESULT   same as calling the function directly; unknown tool name -> {"error": "unknown tool ..."}.
    """
    raise NotImplementedError
