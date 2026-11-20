"""Unit tests for SignalReproducibility. POL-001 and POL-002."""

from sandbox_validation import SignalReproducibility


def _runs(flags: list[bool], *, telemetry: bool = True) -> dict:
    return {
        "hypothesis_id": "H-1",
        "runs": [{"telemetry_present": telemetry, "signal_observed": flag} for flag in flags],
    }


def test_signalReproducibility_missingTelemetry_blocked():
    """POL-001 signalReproducibility_missingTelemetry_blocked"""
    judge = SignalReproducibility()
    assert judge.judge(evidence_found=False, evidence=None, hypothesis_id="H-1") == "blocked"
    assert judge.judge(evidence_found=True, evidence={"runs": []}, hypothesis_id="H-1") == "blocked"
    assert judge.judge(evidence_found=True, evidence="not-json", hypothesis_id="H-1") == "blocked"
    assert (
        judge.judge(
            evidence_found=True,
            evidence={"hypothesis_id": "H-2", "runs": _runs([True] * 5)["runs"]},
            hypothesis_id="H-1",
        )
        == "blocked"
    )
    assert judge.judge(evidence_found=True, evidence=_runs([True, True], telemetry=False), hypothesis_id="H-1") == "blocked"


def test_signalReproducibility_fourOfFive_support():
    """POL-002 signalReproducibility_fourOfFive_support"""
    result = SignalReproducibility().judge(
        evidence_found=True,
        evidence=_runs([True, True, True, True, False]),
        hypothesis_id="H-1",
    )
    assert result == "support"


def test_signalReproducibility_noneOfFive_contradict():
    """POL-002 signalReproducibility_noneOfFive_contradict"""
    result = SignalReproducibility().judge(
        evidence_found=True,
        evidence=_runs([False, False, False, False, False]),
        hypothesis_id="H-1",
    )
    assert result == "contradict"


def test_signalReproducibility_oneOfFive_inconclusive():
    """POL-002 signalReproducibility_oneOfFive_inconclusive"""
    result = SignalReproducibility().judge(
        evidence_found=True,
        evidence=_runs([False, True, False, False, False]),
        hypothesis_id="H-1",
    )
    assert result == "inconclusive"
    short = SignalReproducibility().judge(
        evidence_found=True,
        evidence=_runs([True, True, True]),
        hypothesis_id="H-1",
    )
    assert short == "inconclusive"
