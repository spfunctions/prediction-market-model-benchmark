from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scoring import score_output


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def validate_roster(roster: dict[str, Any]) -> list[dict[str, str]]:
    models = roster.get("models")
    if not isinstance(models, list) or not models:
        raise SystemExit("model roster must contain a non-empty models array")
    normalized: list[dict[str, str]] = []
    for index, row in enumerate(models):
        if not isinstance(row, dict):
            raise SystemExit(f"model roster entry {index} must be an object")
        provider = row.get("provider")
        model = row.get("model")
        if not isinstance(provider, str) or not isinstance(model, str):
            raise SystemExit(f"model roster entry {index} needs provider and model strings")
        normalized.append({"provider": provider, "model": model})
    return normalized


def validate_tasks(tasks: list[dict[str, Any]]) -> None:
    required = {"id", "category", "prompt", "expected", "scoring"}
    seen: set[str] = set()
    for row in tasks:
        missing = required.difference(row)
        if missing:
            raise SystemExit(f"task missing required fields: {sorted(missing)}")
        task_id = row["id"]
        if task_id in seen:
            raise SystemExit(f"duplicate task id: {task_id}")
        seen.add(task_id)


def load_responses(path: Path) -> dict[tuple[str, str], str]:
    rows = load_jsonl(path)
    responses: dict[tuple[str, str], str] = {}
    for row in rows:
        model = row.get("model")
        task_id = row.get("task_id")
        output = row.get("output")
        if not isinstance(model, str) or not isinstance(task_id, str) or not isinstance(output, str):
            raise SystemExit("each response row needs model, task_id, and output strings")
        responses[(model, task_id)] = output
    return responses


def run_benchmark(
    models: list[dict[str, str]],
    tasks: list[dict[str, Any]],
    responses: dict[tuple[str, str], str] | None,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_id = f"{now}-prediction-market"
    results = []
    for model in models:
        model_id = f"{model['provider']}/{model['model']}"
        for task in tasks:
            output = responses.get((model_id, task["id"])) if responses is not None else None
            score = score_output(task["expected"], task["scoring"], output) if output is not None else None
            results.append(
                {
                    "run_id": run_id,
                    "model": model_id,
                    "task_id": task["id"],
                    "status": "ok" if output is not None else "not_run",
                    "output": output,
                    "score": score,
                    "metadata": {"category": task["category"], "scoring": task["scoring"].get("method")},
                }
            )
    scored = [r["score"] for r in results if isinstance(r["score"], (int, float))]
    return {
        "run_id": run_id,
        "task_count": len(tasks),
        "model_count": len(models),
        "scored_count": len(scored),
        "mean_score": sum(scored) / len(scored) if scored else None,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and run the SimpleFunctions prediction-market model benchmark.")
    parser.add_argument("--models", type=Path, default=Path("model_roster.json"))
    parser.add_argument("--tasks", type=Path, default=Path("tasks/prediction_market_seed.jsonl"))
    parser.add_argument("--responses", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=Path("results/dry-run.json"))
    args = parser.parse_args()

    roster = load_json(args.models)
    models = validate_roster(roster)
    tasks = load_jsonl(args.tasks)
    validate_tasks(tasks)

    responses = load_responses(args.responses) if args.responses else None
    output = run_benchmark(models, tasks, responses)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out} with {len(output['results'])} rows, {output['scored_count']} scored")


if __name__ == "__main__":
    main()
