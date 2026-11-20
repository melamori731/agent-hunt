# Assumptions

## Readiness

**Status**: READY_WITH_RISKS

**Work item ID**: LOCAL-dataset-validation

**Base path**: requirements/LOCAL-dataset-validation/

**Generated**: 2026-11-20T18:30:00Z

**Analysis scope**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 3, `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` Dataset Validation loop, `docs/adr/0001-langchain-langgraph.md`, and the user scope for this ticket.

### Summary

Planning can start. The agent tests one stored hypothesis against one labelled dataset fixture and appends one JSON result. Dataset search, sandbox execution, rule specification, abuse classification, shopping-agent launch, faculty reporting, and agent chat are out of scope. ASS-002 quantifies the four result words so they are mutually exclusive.

### Blocking issues

None.

### Tracked risks

- ASS-002: support, contradict, and inconclusive are split by comparing the AI-class rate with the human-class rate. The sources name those outcomes and do not give a numeric cutoff.

---

## Product and requirements assumptions

### ASS-001

- **Statement**: A labelled dataset fixture is a JSON object with `dataset_name` and `rows`, and each row has `label` of `ai` or `human` plus boolean signal fields.
- **Source**: User scope for a labelled dataset fixture; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` Dataset Validation steps 1 and 4
- **Verification**: A fixture with those fields yields numeric class rates, and a fixture without both classes does not.
- **Risk Level**: safe
- **Mitigation**: None

### ASS-002

- **Statement**: The signal is present at a measured rate when its AI-class prevalence is strictly greater than its human-class false-positive rate, the labels refute the signal when prevalence is strictly less, and equal rates mean the dataset cannot decide.
- **Source**: User definitions of support, contradict, and inconclusive; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` false-positive rate formula
- **Verification**: Fixtures with a higher AI rate, a higher human rate, and equal rates store support, contradict, and inconclusive.
- **Risk Level**: risky
- **Mitigation**: Keep the comparison in one policy and acknowledge it before implementation.

### ASS-003

- **Statement**: This agent reads `hypothesis_id` and the signal field name from the orchestrator assignment and does not open another component's hypothesis file.
- **Source**: User scope forbidding imports of other component packages
- **Verification**: A result records the assignment's `hypothesis_id` without importing another package.
- **Risk Level**: safe
- **Mitigation**: None

---

## Architecture assumptions

### ASS-ARCH-001

- **Statement**: Dataset validation is one LangGraph node that calls a LangChain tool to count labelled rows and writes JSON.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user instruction not to revisit that framework
- **Scope**: `dataset_validation`
- **Risk Level**: safe
- **Impact if false**: The node would not match the accepted framework decision.

---

## Open questions

### Critical (blocking planning)

None.

### Important (should resolve early)

None.

### Minor (can defer)

None.

---

## Summary

| Category | Safe | Risky | Blocking | Total |
|----------|------|-------|----------|-------|
| Product assumptions | 2 | 1 | 0 | 3 |
| Architecture assumptions | 1 | 0 | 0 | 1 |
| Open questions | - | - | - | 0 |

---

## Top priorities

| ID | Priority | Why it matters |
|----|----------|----------------|
| REQ-001 | critical | Support is the outcome that says the signal is present at a measured rate. |
| REQ-002 | critical | Contradict is the outcome that says the labels refute the signal. |
| REQ-004 | critical | A missing dataset must be blocked rather than filled in. |
| REQ-007 | critical | Downstream readers depend on the five JSON fields. |
| INV-001 | critical | A result outside the four allowed values cannot be coordinated. |
| POL-002 | critical | The rate comparison is what makes support, contradict, and inconclusive exclusive. |

---

## Autonomous handoff

- **Next stage**: planner
- **Proceed automatically**: yes
- **Planner input path**: requirements/LOCAL-dataset-validation/
- **Reason if paused**: None
