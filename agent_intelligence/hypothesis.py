"""Sourced shopping-session hypotheses and unresolved investigations."""

from __future__ import annotations

ABUSE_CLASSIFICATIONS = {"abusive", "malicious", "legitimate"}
ABUSE_PURPOSES = {"abuse_classification", "abusive_versus_legitimate"}
UNRESOLVED_REASON = (
    "Retrieved sources do not support a testable shopping-session signal."
)


class HypothesisRejection(ValueError):
    """A hypothesis must not be stored."""

    def __init__(self, message: str, *, duplicate: bool = False):
        super().__init__(message)
        self.duplicate = duplicate


class HypothesisRecord:
    """Accept a sourced hypothesis or an unresolved investigation.

    Encapsulates INV-001, INV-002, POL-001, and POL-002. This class rejects
    empty sources, abuse or legitimacy labels, duplicate signals, and incomplete
    hypothesis fields. Weak sources become an unresolved investigation only.
    """

    def __init__(self, store=None):
        self._store = store
        self._hypotheses: list[dict] = []
        self._unresolved: list[dict] = []

    @property
    def hypotheses(self) -> list[dict]:
        if self._store is None:
            return list(self._hypotheses)
        return self._store.read_hypotheses()

    @property
    def unresolved_investigations(self) -> list[dict]:
        if self._store is None:
            return list(self._unresolved)
        return self._store.read_unresolved_investigations()

    def submit(self, draft: dict) -> dict:
        if not isinstance(draft, dict):
            raise HypothesisRejection("A hypothesis record must be a document.")
        self._reject_abuse(draft)
        sources = self._sources(draft)
        if not any(self._supports_signal(source) for source in sources):
            return self._store_unresolved(draft, sources)
        signal = self._required_text(draft, "signal")
        observation = self._required_text(draft, "observation")
        measurements = self._required_measurements(draft)
        cited = self._cited_sources(sources)
        if self._already_stored(draft.get("assistantName"), signal):
            raise HypothesisRejection(
                "A hypothesis for this assistant and signal is already stored.",
                duplicate=True,
            )
        record = {
            "recordType": "hypothesis",
            "assistantName": draft.get("assistantName"),
            "signal": signal,
            "observation": observation,
            "sources": cited,
            "measurements": measurements,
        }
        if self._store is None:
            self._hypotheses.append(record)
        else:
            self._store.write_hypothesis(record)
        return {"outcome": "hypothesis", "record": record}

    def _reject_abuse(self, draft: dict) -> None:
        classification = str(draft.get("classification") or "").strip().lower()
        purpose = str(draft.get("purpose") or "").strip().lower()
        if classification in ABUSE_CLASSIFICATIONS or purpose in ABUSE_PURPOSES:
            raise HypothesisRejection(
                "A hypothesis must not classify an assistant as abusive, malicious, or legitimate."
            )

    def _sources(self, draft: dict) -> list[dict]:
        sources = draft.get("sources", None)
        if "sources" not in draft or sources is None or not isinstance(sources, list):
            raise HypothesisRejection("A hypothesis requires sources.")
        if len(sources) == 0:
            raise HypothesisRejection("A hypothesis requires at least one source.")
        return sources

    def _supports_signal(self, source: dict) -> bool:
        return isinstance(source, dict) and source.get("supportsTestableSignal") is True

    def _required_text(self, draft: dict, field: str) -> str:
        value = draft.get(field)
        if not isinstance(value, str) or not value.strip():
            raise HypothesisRejection(f"A hypothesis requires {field}.")
        return value

    def _required_measurements(self, draft: dict):
        value = draft.get("measurements")
        if value is None or value == "" or value == []:
            raise HypothesisRejection("A hypothesis requires measurements.")
        if not isinstance(value, (str, list)):
            raise HypothesisRejection("A hypothesis requires measurements.")
        return value

    def _cited_sources(self, sources: list[dict]) -> list[dict]:
        cited = []
        for source in sources:
            if not isinstance(source, dict):
                raise HypothesisRejection("A hypothesis requires sources.")
            url = source.get("url")
            title = source.get("title")
            url_ok = isinstance(url, str) and url.strip()
            title_ok = isinstance(title, str) and title.strip()
            if not url_ok or not title_ok:
                raise HypothesisRejection("A hypothesis source requires a URL and a title.")
            cited.append({"url": url, "title": title})
        return cited

    def _already_stored(self, assistant_name, signal: str) -> bool:
        return any(
            item.get("assistantName") == assistant_name and item.get("signal") == signal
            for item in self.hypotheses
        )

    def _store_unresolved(self, draft: dict, sources: list[dict]) -> dict:
        record = {
            "recordType": "unresolved_investigation",
            "assistantName": draft.get("assistantName"),
            "sources": self._cited_sources(sources),
            "reason": UNRESOLVED_REASON,
        }
        if self._store is None:
            self._unresolved.append(record)
        else:
            self._store.write_unresolved_investigation(record)
        return {"outcome": "unresolved", "record": record}
