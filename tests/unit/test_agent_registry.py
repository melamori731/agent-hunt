"""Unit tests for AgentRegistry. INV-003, POL-003."""

import pytest

from agent_intelligence.registry import (
    DISCOVERY_ORIGIN,
    ORCHESTRATOR_ORIGIN,
    AgentRegistry,
    RegistryRejection,
)

SOURCES = [{"url": "https://example.test/muse", "title": "Muse shopping assistant notes"}]


def agentRegistry_addition_createsOneReport():
    """INV-003. One addition yields one report."""
    registry = AgentRegistry()
    result = registry.add("Muse", SOURCES, ORCHESTRATOR_ORIGIN)
    assert len(registry.reports) == 1
    assert len(registry.entries) == 1
    assert result["report"]["assistantName"] == "Muse"
    assert result["report"]["sources"] == SOURCES
    assert result["report"]["origin"] == ORCHESTRATOR_ORIGIN
    assert result["entry"]["assistantName"] == "Muse"


def agentRegistry_secondReport_rejected():
    """INV-003. A second report for the same addition is rejected."""
    registry = AgentRegistry()
    registry.add("Muse", SOURCES, ORCHESTRATOR_ORIGIN)
    with pytest.raises(RegistryRejection):
        registry.add("Muse", SOURCES, DISCOVERY_ORIGIN)
    assert len(registry.reports) == 1
    assert len(registry.entries) == 1


def agentRegistry_eitherOrigin_requiresNameSourcesAndOrigin():
    """POL-003. Both origins fail when name, sources, or origin is missing."""
    for origin in (ORCHESTRATOR_ORIGIN, DISCOVERY_ORIGIN):
        registry = AgentRegistry()
        with pytest.raises(RegistryRejection):
            registry.add("", SOURCES, origin)
        with pytest.raises(RegistryRejection):
            registry.add("Muse", [], origin)
        with pytest.raises(RegistryRejection):
            registry.add("Muse", SOURCES, "")
        assert registry.reports == []
        assert registry.entries == []
