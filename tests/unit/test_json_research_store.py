"""Unit tests for JsonResearchStore."""

from agent_intelligence import JsonResearchStore


def jsonResearchStore_reopen_returnsWrittenRecords(tmp_path):
    """Four written record types are readable from a new store on the same directory."""
    entry = {
        "recordType": "registry_entry",
        "assistantName": "Muse",
        "sources": [{"url": "https://example.test/muse", "title": "Muse notes"}],
    }
    report = {
        "recordType": "registry_report",
        "assistantName": "Muse",
        "sources": entry["sources"],
        "origin": "orchestrator assignment",
    }
    hypothesis = {
        "recordType": "hypothesis",
        "assistantName": "Muse",
        "signal": "navigator.webdriver is true at checkout",
        "observation": "The flag is true.",
        "sources": entry["sources"],
        "measurements": ["share of sessions"],
    }
    unresolved = {
        "recordType": "unresolved_investigation",
        "assistantName": "Other",
        "sources": [{"url": "https://example.test/other", "title": "Other notes"}],
        "reason": "Retrieved sources do not support a testable shopping-session signal.",
    }
    writer = JsonResearchStore(tmp_path)
    writer.write_registry_entry(entry)
    writer.write_registry_report(report)
    writer.write_hypothesis(hypothesis)
    writer.write_unresolved_investigation(unresolved)
    reopened = JsonResearchStore(tmp_path)
    assert reopened.read_registry_entries() == [entry]
    assert reopened.read_registry_reports() == [report]
    assert reopened.read_hypotheses() == [hypothesis]
    assert reopened.read_unresolved_investigations() == [unresolved]
    names = {path.name for path in tmp_path.iterdir()}
    assert names == {
        JsonResearchStore.REGISTRY_ENTRIES,
        JsonResearchStore.REGISTRY_REPORTS,
        JsonResearchStore.HYPOTHESES,
        JsonResearchStore.UNRESOLVED,
    }
