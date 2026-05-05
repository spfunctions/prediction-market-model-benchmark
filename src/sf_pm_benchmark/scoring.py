from __future__ import annotations

import json
import re
from typing import Any


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def extract_json_object(output: str) -> Any:
    output = output.strip()
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass
    start = output.find("{")
    end = output.rfind("}")
    if start >= 0 and end > start:
        return json.loads(output[start : end + 1])
    raise ValueError("no JSON object found")


def json_contains(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(key in actual and json_contains(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) < len(expected):
            return False
        return all(json_contains(a, e) for a, e in zip(actual, expected))
    if isinstance(expected, float):
        try:
            return abs(float(actual) - expected) <= 1e-6
        except (TypeError, ValueError):
            return False
    return actual == expected


def score_output(expected: dict[str, Any], scoring: dict[str, Any], output: str | None) -> float | None:
    if output is None:
        return None

    method = scoring.get("method")
    expected_value = expected.get("value")

    if method == "exact_match":
        return 1.0 if normalize_text(output) == normalize_text(str(expected_value)) else 0.0

    if method == "contains":
        return 1.0 if normalize_text(str(expected_value)) in normalize_text(output) else 0.0

    if method == "label_match":
        label = normalize_text(str(expected_value))
        head = normalize_text(output).split(" ", 1)[0].strip(".,:;")
        return 1.0 if head == label.lower() or label in normalize_text(output[:80]) else 0.0

    if method == "json_exact":
        try:
            return 1.0 if extract_json_object(output) == expected_value else 0.0
        except (json.JSONDecodeError, ValueError):
            return 0.0

    if method == "json_subset":
        try:
            return 1.0 if json_contains(extract_json_object(output), expected_value) else 0.0
        except (json.JSONDecodeError, ValueError):
            return 0.0

    if method == "range":
        match = re.search(r"-?\d+(?:\.\d+)?", output)
        if not match:
            return 0.0
        value = float(match.group(0))
        return 1.0 if float(expected["min"]) <= value <= float(expected["max"]) else 0.0

    raise ValueError(f"unknown scoring method: {method}")
