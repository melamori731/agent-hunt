"""Unit tests for AgentIntelligenceNode. INV-004."""

import pytest

from agent_intelligence import (
    AgentIntelligenceNode,
    DeployedRuleRejected,
    DirectHumanInputRejected,
    JsonResearchStore,
)
from tests.support import MUSE_SOURCE, muse_page, orchestrator_assignment


def _node(tmp_path):
    store = JsonResearchStore(tmp_path)
    return store, AgentIntelligenceNode(store, source_catalog=[muse_page()])


def agentIntelligenceNode_completedRun_writesNoDeployedRule(tmp_path):
    """INV-004. A finished run adds none of a deployed detection rule."""
    store, node = _node(tmp_path)
    result = node.run_assignment(orchestrator_assignment())
    names = {path.name for path in store.directory.iterdir()}
    assert "deployed_rule.json" not in names
    assert not any("deployed" in name for name in names)
    assert names <= {
        JsonResearchStore.REGISTRY_ENTRIES,
        JsonResearchStore.REGISTRY_REPORTS,
        JsonResearchStore.HYPOTHESES,
        JsonResearchStore.UNRESOLVED,
    }
    assert "Thought:" in result["reactTrace"]
    assert "Action: search_public_sources" in result["reactTrace"]
    assert "Observation:" in result["reactTrace"]
    with pytest.raises(DeployedRuleRejected):
        node.write_deployed_rule({"name": "block-webdriver"})
    assert not (store.directory / "deployed_rule.json").exists()


def agentIntelligenceNode_directHumanText_rejected(tmp_path):
    """Human text without an orchestrator assignment is rejected."""
    _store, node = _node(tmp_path)
    with pytest.raises(DirectHumanInputRejected):
        node.run_assignment("Please research Muse.")
    with pytest.raises(DirectHumanInputRejected):
        node.run_assignment({"humanText": "Please research Muse."})
    assert node.store.read_registry_entries() == []


def agentIntelligenceNode_assignment_writesRegistryEntry(tmp_path):
    """An assignment naming an assistant writes one sourced registry entry."""
    store, node = _node(tmp_path)
    node.run_assignment(orchestrator_assignment())
    entries = store.read_registry_entries()
    assert len(entries) == 1
    assert entries[0]["assistantName"] == "Muse"
    assert entries[0]["sources"] == [MUSE_SOURCE]
