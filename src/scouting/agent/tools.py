"""Module 7a - Tools the scouting agent can call.

Keep each tool a thin, deterministic wrapper over the analytics modules (they return JSON-serialisable
dicts). The LLM should never compute stats itself - it chooses which tool to call and explains results.

Design points to think through: tool descriptions/JSON schemas (the model only sees these), small
outputs (don't dump 500 rows into context), explicit errors the model can recover from.
"""
from __future__ import annotations

TOOL_SCHEMAS: list[dict] = [
    # TODO: {"name": "get_team_profile", "description": "...", "input_schema": {...}} - one per tool below
]


def get_team_profile(team: str, season: str) -> dict:
    """Style cluster, formation usage, peers, extreme style axes."""
    raise NotImplementedError


def get_positional_needs(team: str, season: str, top_n: int = 5) -> list[dict]:
    raise NotImplementedError


def search_candidates(role: str, max_age: int, min_minutes: int, leagues: list[str] | None = None, limit: int = 10) -> list[dict]:
    raise NotImplementedError


def compare_players(player_a: str, player_b: str, season: str) -> dict:
    raise NotImplementedError


def similar_to(player: str, season: str, k: int = 5) -> list[dict]:
    raise NotImplementedError


def dispatch(tool_name: str, tool_input: dict):
    """Route a tool call from the model to the function above."""
    raise NotImplementedError
