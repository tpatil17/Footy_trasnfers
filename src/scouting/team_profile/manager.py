"""MODULE 3b - MANAGER PROFILE (optional, do after 3a works).

WHY THIS MODULE EXISTS
    A manager's tactical habits follow him from club to club, while squads change. If United's manager has
    a consistent style at previous clubs, that style tells you what kind of players he wants - even
    if this season's squad does not yet play that way.

CONFIG   manager_profiling in config.yaml:
         lookback_seasons: 5            only use the last 5 seasons
         time_decay_factor: 0.85        each older season counts 15% less
         national_team_weight_discount: 0.30   national-team matches are down-weighted (weak signal)

INPUT    manager tenures (who managed which club in which match) - NOT in the repo yet. You need a source
         (Transfermarkt, Wikipedia, ESPN). Start by hand-entering the current United manager's career.
OUTPUT   one style vector per manager using the SAME features as team_profile/style.py.

HOW TO TEST / EXPECTED RESULT   see each function.
"""
from __future__ import annotations

import pandas as pd


def load_manager_tenures() -> pd.DataFrame:
    """Table of manager spells.

    GOAL     columns: manager, club, start_date, end_date, is_national_team (bool).
    HOW TO TEST
        t = load_manager_tenures(); t[t.manager == "<current United manager>"]
    EXPECTED RESULT
        his full career within the last 5 seasons, dates in order, no overlapping spells, current job has an
        open end date (NaT).
    """
    raise NotImplementedError


def manager_style_profile(manager: str, match_features: pd.DataFrame, tenures: pd.DataFrame) -> pd.Series:
    """Weighted style vector for one manager.

    GOAL     weighted average of the team style features over the matches he managed.
             weight = time_decay_factor ** seasons_ago, multiplied by (1 - national_team_weight_discount)
             for national-team matches.
    OUTPUT   Series indexed by feature name (same names as the style matrix columns).

    HOW TO TEST
        p = manager_style_profile("<manager>", match_features, tenures)
        # compare with United's current vector: how far apart are they?
        # sanity: set decay = 1.0 and discount = 0 -> equals the plain mean over all his matches

    EXPECTED RESULT
        a vector with no NA; with decay=1 and discount=0 it equals the plain average (unit test this);
        with decay=0.85 the most recent season carries clearly more weight. If his profile is far from
        United's current vector, that is itself a finding: the squad does not yet fit his system.
    CAUTION  few matches => noisy. Report how many matches back each profile.
    """
    raise NotImplementedError
