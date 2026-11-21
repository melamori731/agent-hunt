# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Registry entries

#### REQ-001

- **Statement**: When a stored hypothesis and a discovered dataset satisfy every suitability check for that hypothesis, the agent writes one `datasets.json` entry that contains the dataset name, the source URL, the title, suitability `suitable`, and that hypothesis id.
- **Source**: User role for LOCAL-dataset-discovery; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 3; `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` architecture change
- **Verification**: Provide one stored hypothesis and one candidate that has labels, a session identifier, a license, a current verification date, and the hypothesis measurement fields, then confirm one entry contains those five values.
- **Dependencies**: INV-001, POL-001

#### REQ-002

- **Statement**: When a discovered dataset is only a query match, or it lacks a human label, an agent label, a session identifier, a license, a verification date inside the age window, or a hypothesis measurement field, the agent writes one `datasets.json` entry for that hypothesis with suitability `unsuitable`.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` dataset suitability stage; `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 1
- **Verification**: Provide one query-only candidate and one candidate missing a required label, and confirm both entries record suitability `unsuitable` for the hypothesis id.
- **Dependencies**: INV-002, POL-001

#### REQ-003

- **Statement**: Repeating discovery for the same dataset name and the same hypothesis id leaves one `datasets.json` entry for that pair.
- **Source**: `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` architecture change
- **Verification**: Run discovery twice for one dataset and one hypothesis and confirm the registry length for that pair stays one.
- **Dependencies**: POL-002

#### REQ-004

- **Statement**: When no discovered dataset satisfies the suitability checks for a hypothesis, `datasets.json` contains no entry for that hypothesis whose suitability is `suitable`.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` dataset validation step 3; `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 1
- **Verification**: Provide only failing candidates for one hypothesis and confirm zero entries for that hypothesis have suitability `suitable`.
- **Dependencies**: POL-001

### Discovery trigger

#### REQ-005

- **Statement**: The agent searches datasets for a stored hypothesis when the configured interval since the previous scheduled search has elapsed, or when that hypothesis has no suitable registry entry, and that interval defaults to 24 hours.
- **Source**: `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 2; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 6
- **Verification**: With a suitable entry already stored, confirm a search does not run at 23 hours and does run at 24 hours. With no suitable entry, confirm a search runs before the interval elapses.
- **Dependencies**: REQ-001

### Input and output boundary

#### REQ-006

- **Statement**: The agent rejects human text and reads hypothesis records only from stored JSON.
- **Source**: User decision 2026-11-20 that human input enters only through the research orchestrator; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: Call discovery with human text and confirm no `datasets.json` entry is written. Call discovery with a hypothesis file and no human text and confirm the hypothesis is read.
- **Dependencies**: POL-003

#### REQ-007

- **Statement**: A discovery run does not start a shopping agent, does not store a hypothesis, does not store a validation metric, and does not store a deployed detection rule.
- **Source**: User decision 2026-11-20; `docs/adr/0001-langchain-langgraph.md`; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 3
- **Verification**: Run discovery once and confirm no shopping-agent process starts and the store gains no hypothesis, validation-metric, or deployed-rule record.
- **Dependencies**: INV-003, POL-004

---

## Summary

| Verified | Total |
|----------|-------|
| 7 | 7 |
