"""MODULE 1a - CLEAN: turn the raw FBref tables into ONE clean player-season table.

WHY THIS MODULE EXISTS
    Every later module (features, team profile, needs, scoring) needs a single trustworthy table with
    one row per player per club per season. The raw files in data/raw/ are not that yet.

THE FOUR PROBLEMS YOU ARE FIXING (all verified in the raw data)
    1. Bundesliga rows have league = <NA>   (929 of 5158 rows in player_standard; also team tables)
    2. `pos` is messy text: "FW,MF", "MF,DF" ...
    3. The stats are spread over several files (standard, shooting, misc, playing_time).
    4. Players who changed club mid-season appear once per club (149 players in 2526, 35 in 2627).

FUNCTION ORDER (each one feeds the next)
    fix_missing_league -> normalise_positions -> merge_player_tables -> aggregate_multi_club
    and build_player_season_table() runs them all and saves the result.

ONE-TIME SETUP SO YOU CAN IMPORT AND TEST
    source .venv/bin/activate && pip install -e .

HOW TO RUN A SINGLE FUNCTION (pattern used in every function below)
    * Quick look:  open a notebook (kernel = .venv), then
          %load_ext autoreload
          %autoreload 2
          from scouting.config import read_raw
          from scouting.data.clean import fix_missing_league
      ... call the function and inspect the output. `%autoreload 2` re-reads clean.py after each edit.
    * Pass/fail:   delete the `@TODO` line above the matching test in tests/test_acceptance.py, then
          pytest -q tests/test_acceptance.py -k <test name>
"""
from __future__ import annotations

import pandas as pd

KEYS = ["league", "season", "team", "player"]


def fix_missing_league(df: pd.DataFrame, schedules: pd.DataFrame) -> pd.DataFrame:
    """Fill the NA `league` values by looking the team up in the schedules table.

    GOAL
        Every row must end up with a league. The schedules table never has NA leagues, so use it as the
        team -> league lookup (schedules has `league` and `home_team`; every team plays at home).

    INPUT   df: any raw player/team table that has `team` and `league` columns
            schedules: read_raw("schedules")
    OUTPUT  the same table, same number of rows, with `league` filled in. Do not mutate the caller's
            DataFrame (start with df = df.copy()).

    HOW TO TEST
        df = read_raw("player_standard")
        out = fix_missing_league(df, read_raw("schedules"))
        out.league.value_counts(dropna=False)
        # repeat for read_raw("team_standard") and the other raw tables
        pytest -q tests/test_acceptance.py -k no_na_league

    EXPECTED RESULT (player_standard, 5158 rows)
        ITA-Serie A 1115 | ESP-La Liga 1103 | ENG-Premier League 1015 | FRA-Ligue 1 996 | GER-Bundesliga 929
        zero NA values; row count unchanged (5158); Bayern Munich -> GER-Bundesliga.
        Other raw tables: player_playing_time has 6335 rows and 1079 NA leagues before the fix, 0 after.

    COMMON MISTAKE  `team` is the column that exists in the player/team tables; `home_team` only exists
        in schedules. Mapping with df["home_team"] raises KeyError.
    """
    category_map = schedules.set_index("home_team")["league"].to_dict()
    df["league"] = df["league"].fillna(df["home_team"].map(category_map))
    return df



def normalise_positions(df: pd.DataFrame) -> pd.DataFrame:
    """Split the messy raw `pos` text into two clean columns.

    GOAL
        "FW,MF" means primary FW, secondary MF. A single token like "DF" has no secondary.
        Later modules group players by pos_primary, so it must only ever contain GK/DF/MF/FW.

    INPUT   df with a `pos` string column
    OUTPUT  df plus two new columns: `pos_primary` (GK/DF/MF/FW) and `pos_secondary` (same set, or NA).
            Keep the original `pos` column.

    HOW TO TEST
        out = normalise_positions(read_raw("player_standard"))
        out.pos_primary.value_counts(dropna=False)
        out.loc[out.pos == "FW,MF", ["pos", "pos_primary", "pos_secondary"]].head()
        pytest -q tests/test_acceptance.py -k positions_normalised

    EXPECTED RESULT (player_standard, 5158 rows)
        pos_primary:  MF 2277 | DF 1577 | FW 971 | GK 333   (sums to 5158, no NA, nothing else)
        pos_secondary is non-NA for 980 rows (the multi-position players), NA for the rest.
        "FW,MF" -> FW / MF.   "DF" -> DF / NA.
    """
    raise NotImplementedError


def merge_player_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Join standard + shooting + misc + playing_time into one wide table.

    GOAL
        One row per player-club-season with all stat columns side by side, so later code never has to
        juggle separate files.

    INPUT   tables = {"standard": df, "shooting": df, "misc": df, "playing_time": df}
            (each already run through fix_missing_league - otherwise NA leagues will not match up)
    OUTPUT  one DataFrame. Join keys: league, season, team, player, born.
            Start from `standard` and LEFT join the others onto it.

    THINGS THAT WILL BITE YOU
        * Columns repeated across tables (age, nation, pos, 90s, CrdY, CrdR ...) -> keep one copy only,
          or the merge creates _x/_y columns.
        * playing_time has 1177 MORE rows than standard: those are squad players with ~0 minutes.
          A left join from standard drops them, which is what we want.
        * 5 rows have NA `born`; pandas merges NA keys with NA keys, but check the row count is still 5158.
        * Rename columns like "Standard_SoT%" or "Standard_Sh/90" to snake_case without % or /
          (e.g. sot_pct, sh_p90) so they are easy to use in code.

    HOW TO TEST
        tables = {n: fix_missing_league(read_raw(f"player_{n}"), read_raw("schedules"))
                  for n in ["standard", "shooting", "misc", "playing_time"]}
        out = merge_player_tables(tables)
        out.shape; out.columns.tolist(); out.duplicated(["league","season","team","player","born"]).sum()
        pytest -q tests/test_acceptance.py -k merge_player_tables

    EXPECTED RESULT
        exactly 5158 rows (same as standard), 0 duplicated keys, no column ending in _x or _y,
        no column name containing '%' or '/', and the minutes / goals / shots / tackles / starts
        columns all present.
    """
    raise NotImplementedError


def aggregate_multi_club(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse mid-season transfers into ONE row per (season, player) for ranking.

    GOAL
        A player who played 900 min for club X and 100 min for club Y should be ranked as one player
        with 1000 minutes. Per-club rows must stay available elsewhere (team analysis needs them),
        so return a NEW table instead of overwriting the input.

    RULE (the important bit)
        SUM the counting stats (minutes, goals, shots ...), then RECOMPUTE the per-90 columns from the
        totals. Never average per-90 values: 0.9 goals/90 over 900 min and 1.8/90 over 100 min is
        11 goals / (1000 / 90) = 0.99, not (0.9 + 1.8) / 2 = 1.35.

    WATCH OUT  5 rows have NA `born`. pandas groupby silently DROPS rows whose key is NA unless you
        pass dropna=False - check that the row count adds up.

    INPUT   merged player table from merge_player_tables
    OUTPUT  one row per (season, player, born); for movers keep the club with the most minutes as
            `team` and add `teams` (list of all clubs).

    HOW TO TEST
        out = aggregate_multi_club(merged)
        out.duplicated(["season", "player", "born"]).sum()
        out[out.player == "<a known mover>"]   # pick one from: merged[merged.duplicated(["season","player","born"], keep=False)]
        pytest -q tests/test_acceptance.py -k multi_club

    EXPECTED RESULT
        zero duplicated (season, player, born); 149 fewer rows in 2526 and 35 fewer in 2627 than the
        merged table; the unit test above passes (11 goals, 1000 minutes, goals_p90 = 0.99).
    """
    raise NotImplementedError


def build_player_season_table() -> pd.DataFrame:
    """Run the whole module and save the result.

    GOAL     One call produces the table every later module reads.
    STEPS    read raw -> fix_missing_league on every table -> normalise_positions -> merge_player_tables
             -> save per-club table to data/interim/player_season_club.parquet
             -> aggregate_multi_club -> save to data/interim/player_season.parquet.
             Use scouting.config.data_dir("interim") for the folder.

    HOW TO TEST
        from scouting.data.clean import build_player_season_table
        df = build_player_season_table()
        df.shape, df.isna().mean().sort_values().tail()
        pd.read_parquet("data/interim/player_season.parquet").shape   # same as df.shape

    EXPECTED RESULT
        two parquet files appear in data/interim/; no NA in league / season / team / player / pos_primary;
        every row has minutes > 0. After this, update the EDA notebook to read data/interim instead of
        raw so the Bundesliga rows show up under their own league.
    """
    raise NotImplementedError
