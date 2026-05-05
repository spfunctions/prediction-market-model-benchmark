# Research Notes

Snapshot date: 2026-05-05.

## Model Roster Sources

This repository mirrors `spfunctions/major-model-benchmark` so general and prediction-market scores can be compared directly.

- OpenAI: API docs recommend `gpt-5.5` as the flagship model for complex reasoning and coding.
- Anthropic: Claude docs list `claude-opus-4-7` as the most capable generally available model.
- Google: Google announced Gemini 3.1 Pro for developers in preview via the Gemini API. Recheck the exact API model code before a paid run.
- xAI: xAI overview lists Grok 4.3 as the current Grok model.
- DeepSeek: DeepSeek V4 Preview docs list `deepseek-v4-pro` and `deepseek-v4-flash`.
- Mistral: Mistral Medium 3.5 docs list `mistral-medium-3.5`.
- Cohere: Cohere docs list `command-a-reasoning-08-2025`.
- Alibaba Qwen: Alibaba Cloud Model Studio docs list `qwen3.6-plus`.
- Moonshot Kimi: Kimi model docs list `kimi-k2.6`.
- MiniMax: MiniMax API docs list `MiniMax-M2.7`.
- Z.AI GLM: Amazon Bedrock model card lists `zai.glm-5`.
- Meta: Meta Llama 4 Maverick model card lists `meta-llama/Llama-4-Maverick-17B-128E-Instruct`.

## Domain Research Sources

- ForecastBench is a dynamic benchmark for LLM forecasting accuracy using market and dataset questions, scored with Brier-style methods: https://www.forecastbench.org/about/
- KalshiBench frames prediction-market questions as epistemic calibration tests and reports calibration metrics such as ECE and Brier Skill Score: https://huggingface.co/papers/2512.16030
- Prediction-market benchmark suites should preserve point-in-time snapshots because market odds, liquidity, and news context change continuously.

## Open Questions

- Add Brier/log-loss scorers before publishing probabilistic leaderboards.
- Add frozen Kalshi and Polymarket snapshots with clear licensing before large public suites.
- Add separate scores for forecast quality and executable trade quality.
