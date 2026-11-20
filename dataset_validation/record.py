"""Dataset result selection."""

from __future__ import annotations

RESULTS = ("support", "contradict", "inconclusive", "blocked")


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class DatasetResultRecord:
    """One dataset_results.json object. INV-001, INV-002, POL-001, POL-002."""

    def __init__(
        self,
        hypothesis_id: str,
        dataset_name: str,
        result: str,
        prevalence: float | None,
        false_positive_rate: float | None,
    ) -> None:
        if result not in RESULTS:
            raise ValueError("result must be support, contradict, inconclusive, or blocked")
        if not hypothesis_id or not dataset_name:
            raise ValueError("hypothesis_id and dataset_name are required")
        self._check_rates(result, prevalence, false_positive_rate)
        self.hypothesis_id = hypothesis_id
        self.dataset_name = dataset_name
        self.result = result
        self.prevalence = prevalence
        self.false_positive_rate = false_positive_rate

    @staticmethod
    def _check_rates(
        result: str,
        prevalence: float | None,
        false_positive_rate: float | None,
    ) -> None:
        both_numbers = _is_number(prevalence) and _is_number(false_positive_rate)
        both_null = prevalence is None and false_positive_rate is None
        if result == "blocked":
            if not both_null:
                raise ValueError("blocked rates are null")
            return
        if result == "inconclusive":
            if both_null or (both_numbers and prevalence == false_positive_rate):
                return
            raise ValueError("inconclusive rates must be equal or both null")
        if not both_numbers:
            raise ValueError("support and contradict require numeric rates")
        if result == "support" and not prevalence > false_positive_rate:
            raise ValueError("support requires a higher prevalence")
        if result == "contradict" and not prevalence < false_positive_rate:
            raise ValueError("contradict requires a lower prevalence")

    @classmethod
    def missing(cls, hypothesis_id: str, dataset_name: str) -> DatasetResultRecord:
        """POL-001: a missing dataset is blocked and does not invent rates."""
        return cls(hypothesis_id, dataset_name, "blocked", None, None)

    @classmethod
    def from_rates(
        cls,
        hypothesis_id: str,
        dataset_name: str,
        prevalence: float | None,
        false_positive_rate: float | None,
    ) -> DatasetResultRecord:
        """POL-002: strict comparison of the two class rates."""
        if prevalence is None or false_positive_rate is None:
            return cls(hypothesis_id, dataset_name, "inconclusive", None, None)
        if prevalence > false_positive_rate:
            result = "support"
        elif prevalence < false_positive_rate:
            result = "contradict"
        else:
            result = "inconclusive"
        return cls(hypothesis_id, dataset_name, result, prevalence, false_positive_rate)

    def to_dict(self) -> dict:
        return {
            "hypothesis_id": self.hypothesis_id,
            "result": self.result,
            "prevalence": self.prevalence,
            "false_positive_rate": self.false_positive_rate,
            "dataset_name": self.dataset_name,
        }
