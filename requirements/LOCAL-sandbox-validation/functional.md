# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Result file

#### REQ-001

- **Statement**: Given a hypothesis file and a saved evidence file, sandbox validation writes `sandbox_results.json` with `hypothesis_id`, `result`, and `evidence_path`, and `result` is `support`, `contradict`, `inconclusive`, or `blocked`.
- **Source**: User decision 2026-11-20; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` sandbox step 6
- **Verification**: Run one hypothesis with a saved evidence file and confirm the three fields and one of the four result values.
- **Dependencies**: INV-002

#### REQ-002

- **Statement**: When the evidence file is missing, sandbox validation writes `result` `blocked` and the supplied `evidence_path`, and it does not start a browser or a shopping agent.
- **Source**: User decision 2026-11-20
- **Verification**: Point at a missing evidence path and confirm `blocked`, that path, and that no process was started.
- **Dependencies**: POL-001, INV-001

### Saved-run judgment

#### REQ-003

- **Statement**: When the saved runs include five telemetry-complete runs of which at least four observe the signal, within the first ten runs, `result` is `support`.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` provisional stopping rule
- **Verification**: Supply five runs with four positive observations and confirm `support`.
- **Dependencies**: POL-002

#### REQ-004

- **Statement**: When at least five saved runs have telemetry and none observe the signal, `result` is `contradict`.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 4, unsuccessful reproduction
- **Verification**: Supply five telemetry-complete runs with no signal and confirm `contradict`.
- **Dependencies**: POL-002

#### REQ-005

- **Statement**: When telemetry is present and the runs neither meet the support threshold nor show a consistent absence, `result` is `inconclusive`.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 4
- **Verification**: Supply five telemetry-complete runs with one positive observation and confirm `inconclusive`.
- **Dependencies**: POL-002

### Excluded outcomes

#### REQ-006

- **Statement**: The result file does not contain an abuse classification or a deployed detection rule.
- **Source**: User decision 2026-11-20; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` initial scope and rule step 6
- **Verification**: Validate one hypothesis and confirm the result file has no abuse label and no deployed-rule field.
- **Dependencies**: INV-002

---

## Summary

| Verified | Total |
|----------|-------|
| 6 | 6 |
