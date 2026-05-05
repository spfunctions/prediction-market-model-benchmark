# Prediction Market Model Benchmark

Open benchmark harness for comparing current major AI models on prediction-market work: forecast calibration, resolution logic, orderbook interpretation, cross-venue equivalence, thesis updates, and trading risk gates.

This repository mirrors the roster from [spfunctions/major-model-benchmark](https://github.com/spfunctions/major-model-benchmark), but the task suite is domain-specific. The goal is to test whether a model can reason like a prediction-market analyst, not whether it can answer generic finance trivia.

## Current Roster

Roster snapshot: `2026-05-05`.

The roster is in [model_roster.json](model_roster.json) and intentionally matches the general benchmark so domain transfer can be measured model by model. See [docs/research-notes.md](docs/research-notes.md) for source notes.

## Task Families

- `resolution`: decide YES, NO, UNRESOLVED, or INVALID from market rules and evidence.
- `calibration`: produce or evaluate probabilistic forecasts with Brier/log-loss style metrics.
- `microstructure`: interpret spreads, depth, fees, stale quotes, and executable edge.
- `cross-venue`: decide whether two contracts are equivalent enough for arbitrage.
- `thesis-update`: revise a probability after new evidence without double-counting.
- `risk`: reject trades that violate bankroll, conviction, liquidity, or operator constraints.
- `evidence`: distinguish independent evidence from duplicated citations.

The seed task suite is [tasks/prediction_market_seed.jsonl](tasks/prediction_market_seed.jsonl). Larger suites should be versioned under `tasks/vYYYY-MM-DD/` and should include point-in-time market snapshots where possible.

## Run

Validate roster/tasks and emit placeholder rows:

```bash
python src/sf_pm_benchmark/runner.py \
  --models model_roster.json \
  --tasks tasks/prediction_market_seed.jsonl \
  --out results/dry-run.json
```

Score a JSONL file of model responses:

```bash
python src/sf_pm_benchmark/runner.py \
  --models model_roster.json \
  --tasks tasks/prediction_market_seed.jsonl \
  --responses examples/responses.seed.jsonl \
  --out results/scored-seed.json
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Why This Exists

Forecasting benchmarks such as ForecastBench show why dynamic, contamination-resistant probability tasks matter. Prediction-market tasks add a second layer: a model must map rules to outcomes, compare non-identical contracts, account for fees and liquidity, and refuse trades where the forecast is not actionable.

This suite is built to expose those failures.

## Benchmark Rules

- Same prompt, same market snapshot, same tool policy, same scoring rubric.
- All market data must be timestamped and immutable for a run.
- Separate probability quality from trading quality: a good forecast can still be a bad trade after spread, fees, liquidity, and risk limits.
- Publish raw outputs before publishing rankings.
- Report refusal/error rate and invalid-trade rate next to forecast scores.

The methodology is in [docs/methodology.md](docs/methodology.md).

## License

MIT.
