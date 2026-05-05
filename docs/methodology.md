# Methodology

Prediction-market evaluation should separate three capabilities:

1. Forecast quality: Does the model assign calibrated probabilities?
2. Market understanding: Does it understand rules, contract boundaries, liquidity, fees, and venue differences?
3. Trade discipline: Does it refuse trades that are not actionable after costs and risk gates?

## Suite Design

Use three task layers:

- `seed`: public tasks that validate the harness.
- `public`: larger reproducible tasks with frozen market snapshots.
- `holdout`: delayed-release or private tasks for leaderboard claims.

Point-in-time tasks should preserve the market snapshot, timestamp, venue, contract text, orderbook state, and evidence set used by every model.

## Scoring

The current scorer supports exact match, substring, label match, JSON exact match, JSON subset, and numeric range. Domain suites should add:

- Brier score for binary forecasts
- log loss for calibrated probability reporting
- executable edge after fees and spread
- invalid trade rate
- rule-resolution accuracy

## Reporting

A leaderboard row should include:

- model and provider
- run timestamp and market snapshot timestamp
- forecast score, trade score, and invalid-trade rate
- refusal/error rate
- latency and estimated cost

## Anti-Patterns

- Treating a correct probability as a profitable trade without fees and liquidity.
- Comparing Kalshi and Polymarket contracts without checking resolution boundaries.
- Letting models use current web data for historical point-in-time snapshots.
- Publishing rankings without raw outputs and scoring code.
