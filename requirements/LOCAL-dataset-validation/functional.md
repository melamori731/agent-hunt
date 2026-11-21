# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Dataset result

#### REQ-001

- **Statement**: When an orchestrator assignment names a hypothesis and a labelled dataset fixture in which the signal is strictly more common in AI-labelled rows than in human-labelled rows, the agent appends a `dataset_results.json` record whose result is support.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 3; user scope that support means the signal is present at a measured rate
- **Verification**: Run one such assignment and read a support record for that `hypothesis_id`.
- **Dependencies**: REQ-007

#### REQ-002

- **Statement**: When that fixture shows the signal is strictly more common in human-labelled rows than in AI-labelled rows, the appended record result is contradict.
- **Source**: User scope that contradict means the labels refute the signal; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` Dataset Validation step 6
- **Verification**: Run one such assignment and read a contradict record for that `hypothesis_id`.
- **Dependencies**: REQ-007

#### REQ-003

- **Statement**: When the dataset file exists but the AI-class rate and the human-class rate cannot be computed, or the two rates are equal, the appended record result is inconclusive.
- **Source**: User scope that inconclusive means the dataset cannot decide; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` Dataset Validation step 6
- **Verification**: Run one equal-rate fixture and one fixture that lacks a class, and read inconclusive for both.
- **Dependencies**: REQ-007

#### REQ-004

- **Statement**: When the assignment names a dataset path and that file is missing, the appended record result is blocked.
- **Source**: User scope that blocked means the dataset is missing; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` Dataset Validation step 3
- **Verification**: Point the assignment at a path that is not a file and read a blocked record.
- **Dependencies**: REQ-007

#### REQ-007

- **Statement**: Every stored dataset result is one JSON object with the fields `hypothesis_id`, `result`, `prevalence`, `false_positive_rate`, and `dataset_name`.
- **Source**: User scope for `dataset_results.json` records
- **Verification**: Read a stored record and confirm those keys are present and no other keys are present.
- **Dependencies**: None

### Scope boundary

#### REQ-005

- **Statement**: The agent does not search for a dataset, start a shopping agent, write a rule specification, classify abuse, or send a message to another agent.
- **Source**: User settled scope; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: Submit each of those requests and confirm no dataset result is stored and no shopping agent is started.
- **Dependencies**: None

#### REQ-006

- **Statement**: A payload that is not an orchestrator assignment stores no dataset result.
- **Source**: User scope that human input reaches this agent only through the orchestrator
- **Verification**: Submit a chat payload and confirm `dataset_results.json` is unchanged.
- **Dependencies**: None

---

## Summary

| Verified | Total |
|----------|-------|
| 7 | 7 |
