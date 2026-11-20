"""Module 7b - The scouting agent: an LLM tool-use loop on top of the analytics.

Flow:  user goal ("build the Man United shortlist") -> agent plans -> calls get_team_profile /
get_positional_needs -> for each need calls search_candidates / compare_players -> returns a
structured shortlist (player, position, why the position needs filling, why this player).

Use the Anthropic Python SDK (add `anthropic` to requirements; key via ANTHROPIC_API_KEY in .env,
which is already gitignored). Model id comes from config.agent.model. Look up current SDK usage in the
Anthropic docs rather than copying old snippets.

What you practise:
  * tool-use loop (stop_reason == "tool_use" -> run tools -> append tool_result -> repeat), with a max-turn cap
  * structured outputs (validate the final answer against a pydantic model; retry on failure)
  * grounding: every claim in the rationale must trace to a number returned by a tool
  * prompt design (system prompt with the club's context and what "good" looks like)
  * cost/latency control (prompt caching for the static system prompt + tool schemas, small tool outputs)
  * guardrails: refuse to invent players/stats; handle tool errors
Deliberate comparison: run the same task with a plain non-agent pipeline (scoring.top_targets +
a single LLM call to write the prose) and evaluate which is better/cheaper.
"""
from __future__ import annotations

from scouting.scoring.ranker import Recommendation


def run_agent(team: str, season: str, max_turns: int = 12) -> list[Recommendation]:
    raise NotImplementedError


def explain_need(need) -> str:
    """Single-shot LLM call: turn a PositionNeed's numeric evidence into 2-3 sentences. Good first LLM exercise."""
    raise NotImplementedError
