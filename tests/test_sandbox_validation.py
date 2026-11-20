"""Unit tests for SandboxValidation. INV-001 and INV-002."""

import ast
import json
import sys
from pathlib import Path

from sandbox_validation import SandboxValidation

SPAWN_EVENTS = {
    "subprocess.Popen",
    "os.system",
    "os.posix_spawn",
    "os.fork",
    "os.forkpty",
    "os.exec",
    "os.spawn",
}
SEEN: list[str] = []


def _audit(event, args):
    if event in SPAWN_EVENTS:
        SEEN.append(event)


sys.addaudithook(_audit)


def test_sandboxValidation_package_doesNotImportSubprocess():
    """INV-001 sandboxValidation_package_doesNotImportSubprocess"""
    root = Path(__file__).resolve().parents[1] / "sandbox_validation"
    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] != "subprocess"
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert module.split(".")[0] != "subprocess"


def test_sandboxValidation_run_doesNotStartProcess(tmp_path: Path):
    """INV-001 sandboxValidation_run_doesNotStartProcess"""
    hypothesis = tmp_path / "hypothesis.json"
    hypothesis.write_text(json.dumps({"hypothesis_id": "H-1"}), encoding="utf-8")
    missing = tmp_path / "no-evidence.json"
    SEEN.clear()
    record = SandboxValidation().run(str(hypothesis), str(missing), str(tmp_path / "out"))
    assert record["result"] == "blocked"
    assert SEEN == []


def test_sandboxValidation_resultFile_hasThreeFields(tmp_path: Path):
    """INV-002 sandboxValidation_resultFile_hasThreeFields"""
    hypothesis = tmp_path / "hypothesis.json"
    evidence = tmp_path / "evidence.json"
    hypothesis.write_text(json.dumps({"id": "H-9"}), encoding="utf-8")
    evidence.write_text(
        json.dumps(
            {
                "hypothesis_id": "H-9",
                "runs": [{"telemetry_present": True, "signal_observed": False}] * 5,
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "out"
    record = SandboxValidation().run(str(hypothesis), str(evidence), str(output))
    assert list(record) == ["hypothesis_id", "result", "evidence_path"]
    assert record["hypothesis_id"] == "H-9"
    assert record["result"] == "contradict"
    assert record["evidence_path"] == str(evidence)
