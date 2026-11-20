# Footy_trasnfers - transfer scouting engine

A scouting agent that, for a given club (starting with Manchester United), analyses how the team plays,
finds the positions that most need improving, and shortlists Big-5-league players who fit the system -
each with the position, why it needs filling, and why that player.

See [docs/ROADMAP.md](docs/ROADMAP.md) for data findings, the module plan and milestones.

## Layout

```
config/config.yaml        all tunables (seasons, thresholds, score weights, agent model)
data/raw|interim|processed  parquet files (gitignored)
src/data/scripts/         FBref ingestion (soccerdata)
src/notebooks/            EDA
src/scouting/             the project package - modules 1-9, stubs to implement
tests/test_acceptance.py  what "done" means for each module
```

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
```

Secrets (e.g. `ANTHROPIC_API_KEY`) go in `.env`, which is gitignored.
