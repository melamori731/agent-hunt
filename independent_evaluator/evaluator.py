"""Check stored stage records and append PASS or REWORK evaluations."""

from __future__ import annotations

import json
from pathlib import Path

RESULTS = ("PASS", "REWORK")
FIELDS = ("hypothesis_id", "stage", "result", "trigger")
OUTCOMES = {"support", "reject", "inconclusive", "blocked"}
ABUSE_LABELS = ("abusive", "malicious", "legitimate")


class EvaluationRecord:
    """Four-field evaluation. INV-002."""

    def __init__(self, hypothesis_id: str, stage: str, result: str, trigger: str) -> None:
        self.hypothesis_id = hypothesis_id
        self.stage = stage
        self.result = result
        self.trigger = trigger

    def as_dict(self) -> dict:
        if not str(self.hypothesis_id).strip() or not str(self.stage).strip():
            raise ValueError("an evaluation requires a hypothesis id and a stage")
        if self.result not in RESULTS:
            raise ValueError("an evaluation result is PASS or REWORK")
        if not str(self.trigger).strip():
            raise ValueError("an evaluation requires a trigger")
        return {
            "hypothesis_id": self.hypothesis_id,
            "stage": self.stage,
            "result": self.result,
            "trigger": self.trigger,
        }

    @classmethod
    def require(cls, row: dict) -> dict:
        if set(row) != set(FIELDS):
            raise ValueError("an evaluation has only hypothesis_id, stage, result, and trigger")
        return cls(row["hypothesis_id"], row["stage"], row["result"], row["trigger"]).as_dict()


class IndependentEvaluator:
    """Judge one stored stage and append one evaluation. INV-001, POL-001 through POL-004."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def evaluate(self, hypothesis_id: str, stage: str) -> dict:
        if self._abuse(hypothesis_id):
            result, trigger = "REWORK", "classification is out of scope"
        else:
            result, trigger = self._judge(hypothesis_id, stage)
        record = EvaluationRecord(hypothesis_id, stage, result, trigger).as_dict()
        return self._append(record)

    def read_evaluations(self) -> list:
        return list(self._rows("evaluations"))

    def _judge(self, hypothesis_id: str, stage: str) -> tuple[str, str]:
        if stage == "hypothesis":
            return self._hypothesis(hypothesis_id)
        if stage == "validation":
            return self._validation(hypothesis_id)
        if stage == "rule_specification":
            return self._rule(hypothesis_id)
        return "REWORK", "stage is not recognized"

    def _hypothesis(self, hypothesis_id: str) -> tuple[str, str]:
        row = self._one("hypotheses", hypothesis_id)
        if row is None:
            return "REWORK", "hypothesis record is missing"
        if not self._any(row.get("sources")):
            return "REWORK", "hypothesis has no sources"
        return "PASS", "hypothesis has sources"

    def _validation(self, hypothesis_id: str) -> tuple[str, str]:
        outcomes: dict[str, str] = {}
        for row in self._rows("validations"):
            if str(row.get("hypothesis_id")) != str(hypothesis_id):
                continue
            kind = row.get("kind")
            if kind in {"dataset", "sandbox"}:
                outcomes[str(kind)] = row.get("outcome")
        dataset = outcomes.get("dataset")
        sandbox = outcomes.get("sandbox")
        if dataset not in OUTCOMES or sandbox not in OUTCOMES:
            return "REWORK", "validation result is missing"
        if {dataset, sandbox} == {"support", "reject"}:
            return "REWORK", "validation pair contradicts"
        return "PASS", "validation pair does not contradict"

    def _rule(self, hypothesis_id: str) -> tuple[str, str]:
        row = self._one("rule_specifications", hypothesis_id)
        if row is None:
            return "REWORK", "rule specification is missing"
        if row.get("deployed") is True:
            return "REWORK", "rule specification is deployed"
        if row.get("submitted") is not True:
            return "REWORK", "rule specification is not submitted"
        if not self._any(row.get("research_sources")):
            return "REWORK", "rule specification lacks research sources"
        if not self._validation_results_present(row.get("validation_results")):
            return "REWORK", "rule specification lacks validation results"
        return "PASS", "rule specification is submitted with citations"

    def _abuse(self, hypothesis_id: str) -> bool:
        for name in ("hypotheses", "validations", "rule_specifications"):
            for row in self._rows(name):
                if str(row.get("hypothesis_id")) != str(hypothesis_id):
                    continue
                if row.get("purpose") == "abuse_classification":
                    return True
                label = str(row.get("classification") or "").lower()
                if label in ABUSE_LABELS:
                    return True
        return False

    def _one(self, name: str, hypothesis_id: str) -> dict | None:
        found = None
        for row in self._rows(name):
            if str(row.get("hypothesis_id")) == str(hypothesis_id):
                found = row
        return found

    def _validation_results_present(self, value: object) -> bool:
        if self._any(value):
            return True
        if not isinstance(value, dict):
            return False
        dataset = str(value.get("dataset_result") or "").strip()
        sandbox = str(value.get("sandbox_result") or "").strip()
        return bool(dataset and sandbox)

    def _any(self, values: object) -> bool:
        if not isinstance(values, list):
            return False
        return any(self._present(item) for item in values)

    def _present(self, item: object) -> bool:
        if isinstance(item, str):
            return bool(item.strip())
        if isinstance(item, dict):
            url = str(item.get("url") or "").strip()
            title = str(item.get("title") or "").strip()
            return bool(url or title)
        return False

    def _rows(self, name: str) -> list:
        path = self.root / f"{name}.json"
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise TypeError(f"{name}.json must be a list")
        return data

    def _append(self, row: dict) -> dict:
        path = self.root / "evaluations.json"
        rows: list = []
        if path.exists():
            rows = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(rows, list):
                raise TypeError("evaluations.json must be a list")
        rows.append(row)
        path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        return row
