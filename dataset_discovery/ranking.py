"""Rank catalog passages in memory with token cosine similarity."""

from __future__ import annotations

import math
import re
from typing import Any

_TOKEN = re.compile(r"[a-z0-9]+")


def rank_passages(passages: object, query: str, limit: int = 5) -> list[dict[str, Any]]:
    if not isinstance(passages, list):
        return []
    query_vector = _vector(query)
    scored: list[tuple[float, int, dict[str, Any]]] = []
    for index, passage in enumerate(passages):
        if not isinstance(passage, dict):
            continue
        text = f"{passage.get('title') or ''} {passage.get('text') or ''}"
        scored.append((_cosine(query_vector, _vector(text)), index, passage))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in scored[:limit]]


def _vector(text: str) -> dict[str, float]:
    counts: dict[str, float] = {}
    for token in _TOKEN.findall(text.lower()):
        counts[token] = counts.get(token, 0.0) + 1.0
    return counts


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(weight * right.get(token, 0.0) for token, weight in left.items())
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
