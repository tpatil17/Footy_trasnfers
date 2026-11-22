"""MODULE 2 - FEATURES: make player numbers fair to compare.

WHY THIS MODULE EXISTS
    Raw totals are not comparable: a player with 3000 minutes has more goals than one with 900, a
    striker is not a defender, and a 90-minute cameo with 1 goal is noise, not a 0.9 goals/90 talent.
    This module turns the clean table (Module 1) into per-90 rates that are reliable and comparable.

INPUT   data/interim/player_season.parquet (from clean.build_player_season_table)
OUTPUT  data/processed/player_features.parquet - same players, with *_p90 columns, shrunk rates and
        within-position percentiles.

FUNCTION ORDER
    minutes_filter -> add_per90 -> shrink_rate -> position_percentiles -> blend_seasons
    (every function is small and testable on a 3-row toy DataFrame before you run it on real data)

HOW TO RUN / TEST  same pattern as Module 1: pip install -e . once, then use a notebook with
    %autoreload 2 for looking at data, and `pytest -q tests/test_acceptance.py -k <name>` for pass/fail.
"""
from __future__ import annotations

import pandas as pd


def add_per90(df: pd.DataFrame, count_cols: list[str], minutes_col: str = "minutes") -> pd.DataFrame:
    """Add a per-90-minutes version of each counting stat.

    GOAL     goals_p90 = goals / (minutes / 90). Lets you compare players with different playing time.
    INPUT    df with a minutes column and the counting columns named in count_cols
    OUTPUT   df plus one new column `<col>_p90` per entry. Minutes == 0 must give NaN, not inf/crash.

    HOW TO TEST
        toy = pd.DataFrame({"minutes": [900, 90, 0], "goals": [9, 1, 0]})
        add_per90(toy, ["goals"])

    EXPECTED RESULT   goals_p90 = [0.9, 1.0, NaN]. All original columns unchanged.
    """
    raise NotImplementedError


def shrink_rate(successes: pd.Series, exposure: pd.Series, prior_mean: float, prior_strength: float) -> pd.Series:
    """Pull small-sample rates toward the average (empirical-Bayes shrinkage).

    GOAL
        Stop low-minute players topping every ranking. Formula:
            shrunk = (successes + prior_mean * k) / (exposure + k)        where k = prior_strength
        `exposure` is in units of 90s (minutes / 90). `k` acts like "k imaginary 90s at the average rate".

    INPUT    successes: counts (goals), exposure: 90s played, prior_mean: league/position average rate,
             prior_strength: k (try 5-10 90s at first)
    OUTPUT   Series of shrunk rates, same index.

    HOW TO TEST
        shrink_rate(pd.Series([3, 300]), pd.Series([1.0, 100.0]), prior_mean=0.3, prior_strength=10)
        pytest -q tests/test_acceptance.py -k shrinkage

    EXPECTED RESULT
        about [0.545, 2.755]. Player A: raw rate 3.0 on 1 x 90 is pulled almost all the way to 0.3.
        Player B: raw rate 3.0 on 100 x 90s barely moves (3.0 -> 2.755).
        Sanity check on real data: after shrinking goals_p90 for forwards, the top-10 list should contain
        regulars with >1500 minutes, not 60-minute substitutes.
    STRETCH  estimate prior_mean and k from the data instead of picking them by hand.
    """
    raise NotImplementedError


def position_percentiles(df: pd.DataFrame, feature_cols: list[str], group_cols: list[str]) -> pd.DataFrame:
    """Rank each player against others in the SAME group (0 = worst, 1 = best).

    GOAL     "75th percentile among defenders in 2526" means more than "0.12 tackles/90".
             Never rank a defender against strikers.
    INPUT    df, the feature columns, and group_cols (e.g. ["pos_primary", "season"])
    OUTPUT   df with each feature column replaced (or suffixed _pct) by its percentile inside its group.

    HOW TO TEST
        toy = pd.DataFrame({"pos": ["DF"]*3 + ["FW"]*3, "x": [1, 2, 3, 100, 200, 300]})
        position_percentiles(toy, ["x"], ["pos"])
        pytest -q tests/test_acceptance.py -k percentiles

    EXPECTED RESULT
        DF and FW both get [0.33, 0.67, 1.0] even though FW values are 100x bigger.
        On real data: every percentile column lies in [0, 1] and the median is about 0.5 in each group.
    """
    raise NotImplementedError


def blend_seasons(df: pd.DataFrame, decay: float) -> pd.DataFrame:
    """Combine a player's seasons into one profile, trusting recent and high-minute seasons more.

    GOAL     2627 has only ~12 matches, so a player's rate should be a weighted mix of 2526 and 2627.
             weight = minutes * decay ** seasons_ago   (seasons_ago = 0 for the newest season).
             Use preprocessing/manager_profiling time_decay_factor (0.85) from config.yaml as `decay`.
    INPUT    df with columns player, born, season, minutes and the per-90 feature columns
    OUTPUT   one row per player with the weighted average of each feature, plus total minutes.

    HOW TO TEST
        toy: one player, 2526 -> rate 1.0 on 3000 min, 2627 -> rate 2.0 on 1000 min, decay 0.85.

    EXPECTED RESULT   blended rate = (3000*0.85*1.0 + 1000*2.0) / (3000*0.85 + 1000) = about 1.28
                      (sits between 1.0 and 2.0, closer to 1.0 because 2526 has far more minutes).
    """
    raise NotImplementedError


def minutes_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only players with enough minutes and in the target age range (reads config.yaml).

    GOAL     Remove players whose numbers are too noisy to trust or who are outside the age window.
    RULES    from config preprocessing: 2526 (full season) needs >= min_minutes_full_season (900);
             2627 (partial) needs >= min_minutes_current_season (450);
             age between age_range.min and age_range.max (18-29 inclusive).
    OUTPUT   filtered df, same columns.

    HOW TO TEST
        out = minutes_filter(pd.read_parquet("data/interim/player_season_club.parquet"))
        out.groupby("season").size()

    EXPECTED RESULT
        On the per-club table (before multi-club aggregation): 2017 rows - 1261 in 2526, 756 in 2627.
        (Minutes rule alone keeps 2635 rows; the age rule removes the rest.)
        Run it on the aggregated table instead and the counts will be slightly different - that is fine.
    """
    raise NotImplementedError
