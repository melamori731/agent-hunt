"""LangChain tool that counts a signal on labelled rows."""

from __future__ import annotations

import json

from langchain_core.tools import tool


@tool
def count_labelled_signal(rows_json: str, signal: str) -> str:
    """Count AI and human rows where the named signal is true."""
    rows = json.loads(rows_json)
    ai_present = ai_total = human_present = human_total = 0
    for row in rows:
        present = row.get(signal) is True
        label = row.get("label")
        if label == "ai":
            ai_total += 1
            ai_present += int(present)
        elif label == "human":
            human_total += 1
            human_present += int(present)
    return json.dumps(
        {
            "ai_present": ai_present,
            "ai_total": ai_total,
            "human_present": human_present,
            "human_total": human_total,
        }
    )
