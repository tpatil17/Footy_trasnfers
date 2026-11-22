# Roadmap: Manchester United scouting agent

Goal: for a target club, analyse how it plays, find where it needs to improve, and output a shortlist of
players from the Big 5 leagues: **player | position | why that position needs filling | why this player**.

## Findings from reviewing the current data (Nov 2026)

Read these before writing any modelling code; they change the plan.

1. **FBref data has no advanced stats.** The raw tables hold goals, assists, shots, cards, fouls, crosses,
   interceptions, tackles won, playing time and on/off. There is no xG/xA, passing, carrying, pressing or
   defensive-action data, and `fbref_schedules` has no formations or lineups. "Understand the system the
   team plays" is not possible from this alone -> Module 1b adds sources.
2. **Bundesliga has `league = <NA>`** in every player/team table (929 player rows, 36 team rows). It is present
   in `fbref_schedules`, so it can be recovered by team -> league mapping.
3. **2627 is a partial season** (max 12 matches / 1080 min) while 2526 is complete. Per-90 rates from 2627 are
   noisy; the blend/shrinkage in Module 2 exists for this.
4. **Mid-season movers appear once per club** (149 players in 2526). Aggregate for ranking, keep per-club rows for team analysis.
5. `Team Success_On-Off` (player_playing_time) is a cheap, useful signal for the impact model - but it is confounded by teammates.
6. `Loader.run_full_ingestion` fetches match logs (`schedule`/`shooting`/`misc`) that are not in `data/raw` yet.
7. The venv lacks scikit-learn/scipy/etc. -> `requirements.txt`.

## Modules, in suggested order

| # | Module (`src/scouting/...`) | You build | ML / AI skills reinforced |
|---|---|---|---|
| 1 | `data/clean.py`, `data/sources.py`, `data/identity.py` | one clean player-season table; extra sources (Understat xG/PPDA, ESPN lineups, SoFIFA, odds-based team strength, market values; see DATASETS.md); cross-source name matching | data quality, joins, fuzzy matching / entity resolution |
| 2 | `features/engineering.py` | per-90s, shrinkage, within-position percentiles, season blending | empirical Bayes, small-sample noise, normalisation, leakage awareness |
| 3 | `team_profile/style.py`, `manager.py` | style vector per team; clusters; United's peers; manager fingerprint | PCA, KMeans vs GMM, silhouette/BIC, UMAP, cluster stability |
| 4 | `needs/analysis.py` | ranked positional needs with evidence | regularised regression on small n, grouped CV, SHAP, bootstrap CIs |
| 5 | `players/roles.py`, `similarity.py` | tactical roles; "plays like X"; system-fit score | clustering within groups, distance metrics, autoencoder/contrastive embeddings (PyTorch) |
| 6 | `scoring/ranker.py` | filters + explainable score, then learned ranking and age curves | learning-to-rank, mixed-effects/GAM, uncertainty |
| 7 | `agent/tools.py`, `scout_agent.py` | LLM tool-use agent over modules 3-6 | tool schemas, agent loop, structured output, grounding, prompt caching |
| 8 | `evaluation/backtest.py` | backtests, ablations, stability, LLM-output grading | time-split validation, ablation design, LLM evals |
| 9 | `reporting/report.py` | CSV + markdown shortlist, radar charts | communicating results |

`pipeline.py` wires the stages; `tests/test_acceptance.py` defines "done" per module (remove the skip marker as you go).

## Suggested milestones

- **M1 - Foundation (modules 1-2):** clean table + Bundesliga fix + Understat data joined. *Done when* `test_no_na_league_after_fix`,
  `test_positions_normalised`, `test_multi_club_rates_recomputed_from_totals` pass and the EDA notebook reads from `data/interim`.
- **M2 - Understand United (module 3):** a notebook that states, with plots, how United plays vs the league and which 5-8 teams are most similar.
- **M3 - Needs (module 4):** ranked needs with evidence you would defend to a human scout. Sanity-check against what you know about the squad.
- **M4 - Candidates (modules 5-6, baseline scoring):** first shortlist from a hand-weighted score. Keep it as the baseline forever.
- **M5 - Agent (module 7):** wrap M2-M4 in tools; compare agent output to the plain pipeline.
- **M6 - Evaluate (module 8):** backtest at least one past window; run ablations; decide what actually adds value.

## Open decisions for you

- **Which extra data sources?** See [DATASETS.md](DATASETS.md) for the rated list and suggested fetch order. Check coverage for 2025-26/2026-27 before committing.
- **Market values / contracts:** soccerdata does not cover these (Transfermarkt). Read the site's terms before scraping, or find a licensed dataset.
- **Past windows for backtesting:** you currently have only two seasons; `manager_profiling.lookback_seasons: 5` and the learned ranker need more history.
- **Budget realism:** do you want fee/wage constraints in the score, or pure footballing fit first? (Suggest the latter.)
