"""Acceptance tests that define 'done' for each module. Remove the skip marker as you implement each one.

Run: pytest -q
"""
import numpy as np
import pandas as pd
import pytest

TODO = pytest.mark.skip(reason="module not implemented yet")


# ---- Module 1: clean ---------------------------------------------------------------------------
@TODO
def test_no_na_league_after_fix():
    from scouting.config import read_raw
    from scouting.data.clean import fix_missing_league

    out = fix_missing_league(read_raw("player_standard"), read_raw("schedules"))
    assert out["league"].notna().all()
    assert (out.loc[out.team == "Bayern Munich", "league"] == "GER-Bundesliga").all()


@TODO
def test_positions_normalised():
    from scouting.data.clean import normalise_positions

    df = pd.DataFrame({"pos": ["FW,MF", "DF", "MF,DF", "GK"]})
    out = normalise_positions(df)
    assert out["pos_primary"].tolist() == ["FW", "DF", "MF", "GK"]
    assert out["pos_secondary"].tolist()[0] == "MF"


@TODO
def test_multi_club_rates_recomputed_from_totals():
    from scouting.data.clean import aggregate_multi_club

    df = pd.DataFrame({
        "season": ["2526"] * 2, "player": ["A"] * 2, "team": ["X", "Y"],
        "minutes": [900, 100], "goals": [9, 2], "goals_p90": [0.9, 1.8],
    })
    out = aggregate_multi_club(df)
    row = out.iloc[0]
    assert row["goals"] == 11 and row["minutes"] == 1000
    assert row["goals_p90"] == pytest.approx(11 / (1000 / 90))  # NOT mean(0.9, 1.8)


# ---- Module 2: features -------------------------------------------------------------------------
@TODO
def test_shrinkage_behaviour():
    from scouting.features.engineering import shrink_rate

    s = shrink_rate(pd.Series([3, 300]), pd.Series([1.0, 100.0]), prior_mean=0.3, prior_strength=10)
    # small sample pulled hard toward prior, large sample barely moves
    assert abs(s[0] - 0.3) < abs(3 - 0.3) * 0.2
    assert s[1] == pytest.approx(3.0, abs=0.35)


@TODO
def test_percentiles_are_within_group():
    from scouting.features.engineering import position_percentiles

    df = pd.DataFrame({"pos": ["DF"] * 3 + ["FW"] * 3, "x": [1, 2, 3, 100, 200, 300]})
    out = position_percentiles(df, ["x"], ["pos"])
    assert out.loc[out.pos == "DF", "x"].max() == pytest.approx(out.loc[out.pos == "FW", "x"].max())


# ---- Module 3: team profile ---------------------------------------------------------------------
@TODO
def test_style_matrix_standardised_and_one_row_per_team_season():
    from scouting.config import read_raw
    from scouting.team_profile.style import build_style_matrix

    m = build_style_matrix({"standard": read_raw("team_standard")})
    assert not m.index.duplicated().any()
    assert np.allclose(m.mean(), 0, atol=1e-6)


# ---- Module 4: needs ----------------------------------------------------------------------------
@TODO
def test_needs_are_ranked_and_explained():
    from scouting.needs.analysis import rank_needs

    needs = rank_needs("Manchester Utd", "2627")
    assert needs == sorted(needs, key=lambda n: n.severity, reverse=True)
    assert all(n.reasons for n in needs), "every need must carry a human-readable reason"


# ---- Module 6/7: end-to-end contract ------------------------------------------------------------
@TODO
def test_recommendations_have_required_fields():
    from scouting.scoring.ranker import top_targets

    recs = top_targets([], pd.DataFrame())
    for r in recs:
        assert r.player and r.role and r.why_position_needed
