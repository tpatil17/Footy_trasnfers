# Free datasets to fetch (scouted 22 Nov 2026)

What the project needs and does not yet have (see [ROADMAP.md](ROADMAP.md)): shot quality (xG/xA), team style
signals (pressing, possession, formations), player value/contract/age data, and team strength. This file rates
each free option by how much it helps, whether it covers the *current* seasons, and what I actually verified.

**How to read the "checked" column**
- ✅ I checked it myself this session (GitHub API, a local library inspection, or one test call).
- 🔎 Taken from web search results only. Treat as likely, not certain.
- ❓ From general knowledge, not confirmed. Verify before relying on it.

## Big finding: FBref no longer has advanced stats

A 2026 roundup says FBref removed xG, progressive passes, pressures etc. on **20 Jan 2026** after Opta ended its data
arrangement ([thestatsapi.com](https://www.thestatsapi.com/blog/best-football-statistics-websites),
[The IX](https://www.theixsports.com/the-ix-soccer/fbrefs-loss-advanced-stats-womens-soccer-data-accessibility/)) 🔎.
That matches your data (no xG, no passing, no defensive actions). Some scrapers still advertise those columns; they look out of date.
**I found no free source with FBref's old depth** (progressive passes, pressures, carries). The realistic substitutes are
Understat (xG/xA only), WhoScored event data (heavy), and open historical event datasets.

## Summary (best first)

| # | Dataset | What it gives you | Usefulness | Current seasons? | Access | Checked |
|---|---|---|---|---|---|---|
| 1 | **Understat** | player xG, xA, npxG, xGChain, xGBuildup; team match xG/xGA/PPDA; shot locations | ★★★★★ | yes (Big 5) | `soccerdata.Understat` | ⚠️ reader failed in my test |
| 2 | **Transfermarkt datasets** (dcaribou) | market value history, contract expiry, transfers, appearances, lineups, clubs | ★★★★★ | yes (weekly refresh claimed) | CSV/DuckDB download | ✅ licence, 🔎 content |
| 3 | **soccerdata: WhoScored** | full event data (passes, pressures, tackles...), injuries/suspensions | ★★★★ | yes | `soccerdata.WhoScored` (Selenium, heavy) | ✅ reader exists, 🔎 active |
| 4 | **soccerdata: ESPN** | lineups and formations per match | ★★★★ | yes | `soccerdata.ESPN` | ✅ reader exists, ❓ coverage |
| 5 | **football-data.co.uk** | results, shots, cards, bookmaker odds (team-strength signal) | ★★★ | yes | `soccerdata.MatchHistory` or CSV | ✅ reader exists, 🔎 free |
| 6 | **SoFIFA / EA FC ratings** | overall, potential, attribute ratings, positions | ★★★ | yes | `soccerdata.SoFIFA` | ✅ reader exists, 🔎 fixed recently |
| 7 | **FPL official API** | PL only: minutes, form, ownership, availability, per-player stats | ★★★ (PL only) | yes | public JSON, no key | 🔎 free, ❓ fields |
| 8 | **Wyscout open dataset** | full event data, one season (2017/18), 4 of the Big 5 | ★★★ (for learning/ML) | no | Figshare download | 🔎 |
| 9 | **StatsBomb / Hudl open data** | event data (+360), selected competitions | ★★ (for learning) | no | GitHub JSON, `statsbombpy` | ✅ coverage |
| 10 | **ClubElo** | team strength ratings | ★★★ | n/a | **currently broken** | ✅ issue found |
| 11 | football-data.org free API | fixtures, standings, squads for 12 competitions | ★ | yes | API key | 🔎 |
| 12 | FBref (existing + remaining pages) | what you already have, plus match lineups/events | ★★ | yes | `soccerdata.FBref` | ✅ issues found |

## Details and how each helps the modules

### 1. Understat - the highest-value gap filler
- **Gives:** per-player xG, xA, npxG, xGChain, xGBuildup (the last two credit players for involvement in chances,
  useful for midfielders/defenders); per-match team xG, xGA, PPDA; shot events with coordinates. Big 5 only, which is exactly your scope.
- **Helps:** Module 3 style vector (pressing = PPDA, chance quality), Module 4 impact model (xG difference is a
  far better target than goal difference, much less noisy), Module 5/6 finishing vs chance quality for forwards.
- **Status:** `soccerdata` v2026.43.0 lists the reader (`read_player_season_stats`, `read_team_match_stats`, `read_shot_events`).
  **My single test call (Premier League, seasons 2025 and 2026) failed with `JSONDecodeError: Expecting value`** for both. I did not
  find an open soccerdata issue for it. A JSON error like this usually means the response was empty or HTML (blocked, rate-limited or
  changed), but the cause is **unconfirmed**. I stopped there rather than probe the site further.
- **Next step for you:** run it yourself once; if it fails, check [soccerdata issues](https://github.com/probberechts/soccerdata/issues),
  try clearing `~/soccerdata` cache, or try a standalone client such as `understatapi`. Read Understat's terms first.
- **Note:** running my test made a dependency (`tls_requests`) download its helper binary into `.venv/` (gitignored).

### 2. Transfermarkt datasets (dcaribou) - market values, contracts, transfer history
- **Gives (per README via search):** games, players, appearances, clubs, valuations and more; 79,000+ games and 37,000+ players in a
  README snapshot 🔎. Offered as CSV, a DuckDB file, or the `transfermarkt_datasets` Python package.
- **Licence:** CC0-1.0 on the repo ✅ ([github.com/dcaribou/transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets)).
  The underlying source is Transfermarkt, so still skim their terms.
- **Freshness:** last repo push 5 Sep 2026 ✅; the README claims weekly data refreshes. **After downloading, check the max date in the
  valuations/appearances tables** to confirm it reaches the 2026-27 season.
- **Helps:** Module 6 hard filters (contract expiry, value), price sanity checks, **backtesting** (past transfers + valuations give you
  history you do not have from FBref), age curves (appearances back to many seasons), Module 1c entity matching (it has player ids/birth dates).
- **Caveat:** hosted API for it is reportedly unavailable; use the file downloads 🔎.

### 3. soccerdata WhoScored - event data and availability
- **Gives:** `read_events` (every pass, tackle, pressure...), `read_missing_players` (injuries/suspensions), `read_schedule`.
  The only route in this list to progressive-pass / defensive-action style features after FBref's removal.
- **Helps:** Module 3 (build possession, directness, defensive line proxies from events), Module 5 (real role discovery), Module 4 (availability risk).
- **Cost:** needs a browser (Selenium) and is slow; a full season is a big download. Event data is huge, so aggregate to per-player/team features
  immediately and keep only those. Use [kloppy](https://github.com/PySport/kloppy) (BSD-3, updated Nov 2026 ✅) to standardise events.
- **Status:** actively maintained (WhoScored fixes merged Oct 2026) ✅. Check the site's terms; scraping heavily is the riskiest option here.

### 4. soccerdata ESPN - lineups and formations
- **Gives:** `read_lineup`, `read_matchsheet`. Targets the "what formation do they play" question that FBref's schedule cannot answer.
- **Helps:** `team_profile.style.infer_formation_usage`, Module 4 (which slots exist), Module 5 (which role slot a player fills).
- **Caveat:** ❓ I did not verify 2025-26/2026-27 coverage or whether formation strings are included. Test one team first
  (FBref's `read_lineup` is an alternative, but FBref has CAPTCHA/scraping issues, see #12).

### 5. football-data.co.uk (`MatchHistory`)
- **Gives:** match results, shots, shots on target, fouls, cards, corners, plus bookmaker odds, free CSVs 🔎. No player data.
- **Helps:** **team strength from closing odds** (implied win probabilities are a strong, cheap strength measure). That fills the hole left by
  ClubElo being down (see #10) and gives you an opposition-strength adjustment for Module 2 and the impact model in Module 4.
- **Status:** `read_games` exists ✅; free per third-party descriptions, read their terms 🔎.

### 6. SoFIFA / EA FC ratings (`soccerdata.SoFIFA`)
- **Gives:** `read_player_ratings`, `read_players`, `read_team_ratings`: overall, potential, attributes, positions.
- **Helps:** a **potential** rating for young targets (not derivable from stats), quality prior for players with few minutes, position labels
  to help Module 5 roles.
- **Caveat:** ratings are partly built from the same performances you are modelling, so use them as a feature/prior, not as ground truth.
  EA's own site shows ratings but not contract or value 🔎. I did not find a trustworthy Kaggle copy; use the reader and check terms.
- **Status:** reader fix was in a recent release (Oct 2026) 🔎.

### 7. FPL official API (Premier League only)
- **Gives:** one public endpoint (`bootstrap-static`) returns all players and clubs of the current season; per-player history from `element-summary`. Free, no key,
  but **undocumented and can change** 🔎. From my knowledge it also carries expected goals/assists and availability flags (❓ check the live response).
- **Helps:** current-season data and availability for **United's own squad and PL candidates** only; useful as a cross-check against your other sources.
- **Historical:** [vaastav/Fantasy-Premier-League](https://github.com/vaastav/Fantasy-Premier-League) holds past FPL seasons (repo updated Oct 2026 ✅; licence unspecified; contents ❓).

### 8. Wyscout open dataset (Pappalardo et al.) - for learning/ML practice
- **Gives:** every event of 2017/18 for Premier League, La Liga, Serie A, Ligue 1 (380 matches each; no Bundesliga) plus World Cup 2018 and
  Euro 2016, as JSON on Figshare. **CC BY 4.0** (cite the paper) 🔎 ([collection](https://figshare.com/collections/_/4415000)).
- **Helps:** you cannot score *current* targets with it, but it is the best free sandbox for Module 5 (role clustering, embeddings, similarity)
  and Module 3 (style from events) with real event data covering a whole season, and for testing methods before paying the cost of scraping WhoScored.

### 9. StatsBomb / Hudl open data
- **Gives:** event data (360 for some) for selected competitions. The repo has moved to `hudl/open-data` ✅ (old link redirects); licence shows as
  non-standard (read their user agreement; attribution is required) ✅.
- **Coverage I verified from `competitions.json`:** Premier League 2003/04 and 2015/16; La Liga many seasons (2004/05 onwards, Messi era);
  Bundesliga 2015/16 and 2023/24 (Leverkusen's season); Ligue 1 2015/16, 2021/22, 2022/23; Serie A 1986/87 and 2015/16; Champions League, World Cup 2018/2022, Euro 2020/2024; women's leagues.
- **Helps:** the same learning-sandbox role as #8 and cleaner event semantics; not suitable for current-window scouting.
- **Access:** `pip install statsbombpy`.

### 10. ClubElo - currently broken
- Team strength ratings. **The API returns 502 for every path** and is reported to have moved behind authentication with no open registration
  ([soccerdata issue #977](https://github.com/probberechts/soccerdata/issues/977), Sept 2026) ✅. `read_by_date` / `read_team_history` therefore do not work.
  The website still shows charts. Use bookmaker-odds-implied strength (#5) or compute your own Elo from results instead.

### 11. football-data.org free API
- 12 competitions, 10 requests/minute, delayed scores, no player-level data such as lineups on the free tier 🔎 (third-party descriptions).
  Redundant with what you already have; skip unless you want squads/fixtures through an official API.

### 12. FBref - existing source, with caveats
- The `soccerdata` FBref reader still works for basic tables (you already pulled them) and also offers `read_lineup` and `read_events`.
- Open issues: **CAPTCHA errors** (#967, Aug 2026) and **team match stats not scraping for four leagues** (#880) ✅. A stale cache can hide
  missing seasons (#987). Your existing parquet files are valuable, so avoid unnecessary re-fetching.

## Gaps nothing free fills well
- Progressive passes, carries, pressures/pressing at FBref's old depth: only recoverable from event data (WhoScored, or open historical sets).
- Wages and fees: not available free from any source I checked.
- Manager tenures (Module 3b): not in any dataset above except partially in Transfermarkt data; plan to hand-enter the current manager's career.

## Suggested fetch order
1. **dcaribou Transfermarkt** - easiest download, unlocks contracts/values/history, no scraping risk.
2. **Understat** - after confirming the reader works for you (highest modelling value).
3. **football-data.co.uk** odds - cheap team-strength signal.
4. **ESPN lineups** - test with one team first.
5. **SoFIFA** - potential ratings.
6. **Wyscout 2017/18 open data** - for Module 5 practice while you wait on slower scraping.
7. **WhoScored events** - only if the above leaves Module 3/5 too weak; budget time and respect rate limits.

Before scraping any site, read its terms and keep requests slow and cached; the `Fbreif_Loader.py` `_save_or_load` pattern already caches to `data/raw/`.
