"""Integration scenarios for sandbox validation. REQ-001 through REQ-006 and QR-001."""

import json
from pathlib import Path

from sandbox_validation import SandboxValidation


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _runs(flags: list[bool]) -> dict:
    return {
        "hypothesis_id": "H-1",
        "runs": [{"telemetry_present": True, "signal_observed": flag} for flag in flags],
    }


def _hypothesis(directory: Path, **extra) -> Path:
    path = directory / "hypothesis.json"
    _write(path, {"hypothesis_id": "H-1", "signal": "vm fingerprint", **extra})
    return path


def test_evidence_present_writesResultFile(tmp_path: Path):
    """REQ-001 evidence_present_writesResultFile"""
    hypothesis = _hypothesis(tmp_path)
    evidence = tmp_path / "evidence.json"
    _write(evidence, _runs([True, True, True, True, False]))
    output = tmp_path / "out"
    record = SandboxValidation().run(str(hypothesis), str(evidence), str(output))
    written = json.loads((output / "sandbox_results.json").read_text(encoding="utf-8"))
    assert record == written
    assert written["hypothesis_id"] == "H-1"
    assert written["result"] == "support"
    assert written["evidence_path"] == str(evidence)


def test_evidence_missing_recordsBlocked(tmp_path: Path):
    """REQ-002 evidence_missing_recordsBlocked"""
    hypothesis = _hypothesis(tmp_path)
    missing = tmp_path / "missing-evidence.json"
    output = tmp_path / "out"
    written_path = output / "sandbox_results.json"
    record = SandboxValidation().run(str(hypothesis), str(missing), str(output))
    assert record["result"] == "blocked"
    assert record["evidence_path"] == str(missing)
    assert record["hypothesis_id"] == "H-1"
    assert json.loads(written_path.read_text(encoding="utf-8"))["result"] == "blocked"


def test_runs_fourOfFive_support(tmp_path: Path):
    """REQ-003 runs_fourOfFive_support"""
    hypothesis = _hypothesis(tmp_path)
    evidence = tmp_path / "evidence.json"
    _write(evidence, _runs([True, False, True, True, True]))
    record = SandboxValidation().run(str(hypothesis), str(evidence), str(tmp_path / "out"))
    assert record["result"] == "support"


def test_runs_noneOfFive_contradict(tmp_path: Path):
    """REQ-004 runs_noneOfFive_contradict"""
    hypothesis = _hypothesis(tmp_path)
    evidence = tmp_path / "evidence.json"
    _write(evidence, _runs([False, False, False, False, False]))
    record = SandboxValidation().run(str(hypothesis), str(evidence), str(tmp_path / "out"))
    assert record["result"] == "contradict"


def test_runs_mixed_inconclusive(tmp_path: Path):
    """REQ-005 runs_mixed_inconclusive"""
    hypothesis = _hypothesis(tmp_path)
    evidence = tmp_path / "evidence.json"
    _write(evidence, _runs([True, False, False, False, False]))
    record = SandboxValidation().run(str(hypothesis), str(evidence), str(tmp_path / "out"))
    assert record["result"] == "inconclusive"


def test_result_file_omitsAbuseAndRule(tmp_path: Path):
    """REQ-006 result_file_omitsAbuseAndRule"""
    hypothesis = _hypothesis(tmp_path, purpose="abuse_classification")
    evidence = tmp_path / "evidence.json"
    _write(evidence, _runs([True, True, True, True, False]))
    output = tmp_path / "out"
    record = SandboxValidation().run(str(hypothesis), str(evidence), str(output))
    assert set(record) == {"hypothesis_id", "result", "evidence_path"}
    assert "abuse" not in record
    assert "deployed" not in record
    assert list(output.iterdir()) == [output / "sandbox_results.json"]


def test_validation_sameEvidence_writesSameResult(tmp_path: Path):
    """QR-001 validation_sameEvidence_writesSameResult"""
    hypothesis = _hypothesis(tmp_path)
    evidence = tmp_path / "evidence.json"
    _write(evidence, _runs([True, True, True, True, False]))
    first = tmp_path / "first"
    second = tmp_path / "second"
    SandboxValidation().run(str(hypothesis), str(evidence), str(first))
    SandboxValidation().run(str(hypothesis), str(evidence), str(second))
    assert (first / "sandbox_results.json").read_bytes() == (second / "sandbox_results.json").read_bytes()
