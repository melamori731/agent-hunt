"""Registry entries and the one human-readable report for each addition."""

from __future__ import annotations

ORCHESTRATOR_ORIGIN = "orchestrator assignment"
DISCOVERY_ORIGIN = "scheduled discovery"
ALLOWED_ORIGINS = {ORCHESTRATOR_ORIGIN, DISCOVERY_ORIGIN}


class RegistryRejection(ValueError):
    """An addition would violate the registry report rules."""


class AgentRegistry:
    """Store one assistant entry and exactly one addition report.

    Encapsulates INV-003 and POL-003. A second report for the same addition
    is rejected. Both origins require the assistant name, cited sources, and origin.
    """

    def __init__(self, store=None):
        self._store = store
        self._entries: list[dict] = []
        self._reports: list[dict] = []

    @property
    def entries(self) -> list[dict]:
        if self._store is None:
            return list(self._entries)
        return self._store.read_registry_entries()

    @property
    def reports(self) -> list[dict]:
        if self._store is None:
            return list(self._reports)
        return self._store.read_registry_reports()

    def add(self, assistant_name: str, sources: list[dict], origin: str) -> dict:
        public_sources = self._require_report_fields(assistant_name, sources, origin)
        if any(entry["assistantName"] == assistant_name for entry in self.entries):
            raise RegistryRejection(
                f"A second report for {assistant_name} is rejected."
            )
        entry = {
            "recordType": "registry_entry",
            "assistantName": assistant_name,
            "sources": public_sources,
        }
        titles = ", ".join(
            f"{source['title']} ({source['url']})" for source in public_sources
        )
        report = {
            "recordType": "registry_report",
            "assistantName": assistant_name,
            "sources": public_sources,
            "origin": origin,
            "summary": f"Added {assistant_name} from {origin}. Sources: {titles}.",
        }
        if self._store is None:
            self._entries.append(entry)
            self._reports.append(report)
        else:
            self._store.write_registry_entry(entry)
            self._store.write_registry_report(report)
        return {"entry": entry, "report": report}

    def _require_report_fields(self, assistant_name, sources, origin) -> list[dict]:
        if not isinstance(assistant_name, str) or not assistant_name.strip():
            raise RegistryRejection("A registry report requires an assistant name.")
        if origin not in ALLOWED_ORIGINS:
            raise RegistryRejection("A registry report requires an entry origin.")
        if not isinstance(sources, list) or len(sources) == 0:
            raise RegistryRejection("A registry report requires cited sources.")
        public_sources = []
        for source in sources:
            if not isinstance(source, dict):
                raise RegistryRejection("A registry report requires cited sources.")
            url = source.get("url")
            title = source.get("title")
            if not isinstance(url, str) or not url.strip():
                raise RegistryRejection("A registry report requires cited sources.")
            if not isinstance(title, str) or not title.strip():
                raise RegistryRejection("A registry report requires cited sources.")
            public_sources.append({"url": url, "title": title})
        return public_sources
