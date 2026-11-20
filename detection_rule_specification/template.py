"""Submitted specification template. Sections are research sources and validation results."""

from __future__ import annotations


class SpecificationTemplate:
    """INV-001, INV-002, INV-003."""

    SECTIONS = ("research_sources", "validation_results")
    RECORD_KEYS = frozenset(
        {
            "hypothesis_id",
            "submitted",
            "deployed",
            "confidence",
            "research_sources",
            "validation_results",
        }
    )
    CLASSIFICATION_KEYS = frozenset(
        {
            "abuse",
            "legitimacy",
            "abuse_classification",
            "legitimacy_classification",
            "classification",
        }
    )

    def build(
        self,
        hypothesis_id: str,
        confidence: str,
        research_sources: list,
        dataset_result: str,
        sandbox_result: str,
    ) -> dict:
        record = {
            "hypothesis_id": hypothesis_id,
            "submitted": True,
            "deployed": False,
            "confidence": confidence,
            "research_sources": [dict(source) for source in research_sources],
            "validation_results": {
                "dataset_result": dataset_result,
                "sandbox_result": sandbox_result,
            },
        }
        self.assert_record(record)
        return record

    def assert_record(self, record: dict) -> None:
        if set(record) & self.CLASSIFICATION_KEYS:
            raise ValueError("a specification has no abuse or legitimacy classification")
        if set(record) != self.RECORD_KEYS:
            raise ValueError("a specification uses the template fields")
        if record["submitted"] is not True or record["deployed"] is not False:
            raise ValueError("a specification is submitted and not deployed")
        if record["confidence"] not in {"standard", "lower"}:
            raise ValueError("confidence is standard or lower")
        sources = record["research_sources"]
        if not isinstance(sources, list) or not sources:
            raise ValueError("a specification includes research sources")
        for source in sources:
            if set(source) != {"url", "title"}:
                raise ValueError("a research source has a url and a title")
            if not str(source["url"]).strip() or not str(source["title"]).strip():
                raise ValueError("a research source has a url and a title")
        results = record["validation_results"]
        if not isinstance(results, dict) or set(results) != {"dataset_result", "sandbox_result"}:
            raise ValueError("validation results include the dataset result and the sandbox result")
        if not str(results["dataset_result"]).strip() or not str(results["sandbox_result"]).strip():
            raise ValueError("validation results include the dataset result and the sandbox result")
