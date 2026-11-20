# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Human input

#### REQ-001

- **Statement**: When a human names an AI assistant, the research orchestrator stores one assignment for the agent-intelligence agent that contains that name, and the orchestrator does not retrieve sources or store a hypothesis.
- **Source**: User decision 2026-11-19; `docs/specs/Multi_Agent_Coordination_Capstone.md` sections 1 and 3
- **Verification**: Submit one assistant name and confirm one assignment record contains that name and that no hypothesis was stored by the orchestrator.
- **Dependencies**: INV-001

#### REQ-002

- **Statement**: When a human asks only to distinguish abusive or malicious AI agents from legitimate AI agents, the orchestrator stores no research assignment.
- **Source**: User decision 2026-11-19
- **Verification**: Submit one abuse-classification request and confirm the assignment count is unchanged.
- **Dependencies**: None

### Standup assignments

#### REQ-003

- **Statement**: When the configured standup interval since the previous standup has elapsed, the orchestrator reads stored hypotheses and validation reports and assigns each hypothesis that is awaiting validation to both dataset validation and sandbox validation.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Orchestrator steps 1–2; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 1
- **Verification**: With the interval set to 1 hour and one hypothesis awaiting validation, confirm that at one hour both assignment records exist, and that at 59 minutes they do not.
- **Dependencies**: POL-001

#### REQ-004

- **Statement**: When one validation result supports a hypothesis and the other is blocked or inconclusive and does not contradict it, the orchestrator stores a rule-specification request and records lower evidence confidence.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Orchestrator step 3; section 4
- **Verification**: Provide one supporting result and one inconclusive result and confirm one rule-specification request marked lower confidence.
- **Dependencies**: REQ-005, POL-001

#### REQ-005

- **Statement**: When the two validation results contradict each other, or the hypothesis is marked insufficiently defined, the orchestrator stores an investigation return and does not store a rule-specification request.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Orchestrator step 4
- **Verification**: Provide contradicting results and confirm an investigation return exists and the rule-specification request count is unchanged.
- **Dependencies**: POL-002

### Stage control

#### REQ-006

- **Statement**: The orchestrator does not advance a task when the independent evaluator result is missing or is not PASS.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` sections 4 and 5
- **Verification**: Advance one task with a PASS result and confirm a second task with a missing result stays in its current stage.
- **Dependencies**: POL-001, INV-001

#### REQ-007

- **Statement**: The orchestrator records a submitted rule specification for human review and does not write a deployed detection rule.
- **Source**: User decision 2026-11-19; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 1
- **Verification**: Finish one eligible standup and confirm the submitted specification is stored and no deployed-rule record exists.
- **Dependencies**: INV-003

#### REQ-008

- **Statement**: When the number of REWORK returns for a task reaches the configured limit, the orchestrator suspends that task for human review instead of returning it again.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Verification**: With the limit set to 2, return a correctable failure a third time and confirm the task is suspended and not reassigned.
- **Dependencies**: POL-002, POL-003

---

## Summary

| Verified | Total |
|----------|-------|
| 8 | 8 |
