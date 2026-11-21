"""Choose standard, lower, or no specification from stored evidence."""

from __future__ import annotations


class EvidenceConfidence:
    """REQ-001, REQ-002, and REQ-003. One place chooses the confidence label."""

    SUPPORT = "support"
    CONTRADICT = "contradict"
    LOWER_OTHER = frozenset({"inconclusive", "blocked"})

    def level(self, dataset_result: str, sandbox_result: str, research_sources: list) -> str | None:
        if not self.sources_complete(research_sources):
            return None
        if dataset_result == self.CONTRADICT or sandbox_result == self.CONTRADICT:
            return None
        if dataset_result == self.SUPPORT and sandbox_result == self.SUPPORT:
            return "standard"
        pair = {dataset_result, sandbox_result}
        if self.SUPPORT in pair and pair <= {self.SUPPORT, *self.LOWER_OTHER} and dataset_result != sandbox_result:
            return "lower"
        return None

    def sources_complete(self, research_sources: list) -> bool:
        if not research_sources:
            return False
        for source in research_sources:
            if not isinstance(source, dict):
                return False
            url = str(source.get("url") or "").strip()
            title = str(source.get("title") or "").strip()
            if not url or not title:
                return False
        return True
