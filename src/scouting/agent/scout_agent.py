"""MODULE 7b - THE SCOUTING AGENT: an LLM that uses the tools to build the shortlist.

WHY THIS MODULE EXISTS
    The analytics already produce a shortlist. The agent adds: deciding what to investigate, comparing
    candidates, and explaining everything in clear football language, grounded in tool results.
    (Deliberately build the plain version first - top_targets + ONE LLM call to write the prose - and
    compare it with the agent version. If the agent is not better or is much more expensive, say so.)

SETUP
    pip install anthropic pydantic python-dotenv
    put ANTHROPIC_API_KEY=... in a .env file in the repo root (it is gitignored - never commit keys)
    model name comes from config.yaml -> agent.model; read the current Anthropic SDK docs for exact call syntax.

THE LOOP (explain this to yourself before coding)
    1. send the user goal + system prompt + tool schemas to the model
    2. if the reply asks to use a tool (stop reason "tool_use"): run it with tools.dispatch,
       append the tool result to the conversation, call the model again
    3. repeat until the model gives a final answer or max_turns is reached (config agent.max_turns = 12)

HOW TO RUN / TEST   start with explain_need (one call, no tools), then run_agent. Costs real money: use a
    cheap model while developing and cap max_turns.
"""
from __future__ import annotations

from scouting.scoring.ranker import Recommendation


def explain_need(need) -> str:
    """Easiest LLM exercise: turn a PositionNeed's numbers into prose.

    GOAL     2-3 sentences explaining why the position needs strengthening, quoting only numbers that are in
             need.evidence / need.reasons.
    HOW TO TEST
        need = rank_needs("Manchester Utd", "2627")[0]
        explain_need(need)
        # check every number in the text appears in need.evidence (write a regex check)
    EXPECTED RESULT
        2-3 readable sentences; every number matches the evidence exactly; no invented stats or players;
        same input twice gives the same facts (wording may vary).
    """
    raise NotImplementedError


def run_agent(team: str, season: str, max_turns: int = 12) -> list[Recommendation]:
    """Run the full tool-using agent.

    GOAL     given a club, the agent calls get_team_profile and get_positional_needs, then for each need uses
             search_candidates / compare_players, and finishes with a structured shortlist.
    OUTPUT   list[Recommendation] - validate the final answer with a pydantic model and retry once if it
             does not parse.
    HOW TO TEST
        recs = run_agent("Manchester Utd", "2627")
        len(recs); [r.player for r in recs]
        # print the list of tool calls the agent made (log them) and read the trace
        # grounding: evaluation.backtest.grounding_check(rationale, tool_outputs)
        # failure test: temporarily make a tool return {"error": ...} - the agent should recover or say it cannot
    EXPECTED RESULT
        finishes in <= 12 turns; 15-25 recommendations, each with player, club, role, why_position_needed and
        why_player_fits; every player exists in your data; every number in the explanations appears in
        some tool output (grounding_check >= 0.95); the tool trace shows the needs were fetched first.
        Typical cost: well under a dollar per run.
    """
    raise NotImplementedError
