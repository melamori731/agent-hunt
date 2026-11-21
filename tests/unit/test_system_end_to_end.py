"""Unit tests for SystemEndToEndTest. POL-004."""

import subprocess

from agent_intelligence import SystemEndToEndTest
from tests.support import write_system_records


def systemEndToEndTest_run_startsNoShoppingAgent(tmp_path, monkeypatch):
    """POL-004. A run performs no shopping-agent process start."""
    write_system_records(tmp_path, include_validation_results=True)
    calls = []

    def record_call(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("shopping agent process start")

    monkeypatch.setattr(subprocess, "Popen", record_call)
    monkeypatch.setattr(subprocess, "run", record_call)
    result = SystemEndToEndTest().run(tmp_path)
    assert calls == []
    assert result["shoppingAgentStarted"] is False
    assert result["passed"] is True


def systemEndToEndTest_missingValidationResults_fails(tmp_path):
    """A specification without validation results fails."""
    write_system_records(tmp_path, include_validation_results=False)
    result = SystemEndToEndTest().run(tmp_path)
    assert result["passed"] is False


def systemEndToEndTest_sameRecords_sameResult(tmp_path):
    """Two runs on the same records return the same pass or fail result."""
    write_system_records(tmp_path, include_validation_results=True)
    tester = SystemEndToEndTest()
    assert tester.run(tmp_path) == tester.run(tmp_path)
