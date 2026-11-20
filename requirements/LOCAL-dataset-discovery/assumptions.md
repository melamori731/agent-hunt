# Assumptions

## Readiness

**Status**: READY_WITH_RISKS

**Work item ID**: LOCAL-dataset-discovery

**Base path**: requirements/LOCAL-dataset-discovery/

**Generated**: 2026-11-20T18:30:00Z

**Analysis scope**: `docs/specs/Multi_Agent_Coordination_Capstone.md`, the other markdown specs under `docs/specs/`, `docs/adr/0001-langchain-langgraph.md`, and the user decisions for this ticket.

### Summary

Dataset discovery can be planned. It reads stored hypothesis JSON, judges dataset suitability, and writes `datasets.json`. It does not research assistants, validate hypotheses, launch a shopping agent, or deploy a rule. The verification age window and the hypothesis field names are tracked risks. No blocking question remains.

### Blocking issues

None.

### Tracked risks

- CA-001: sources name age as a suitability check and do not give a day count.
- CA-002: the hypothesis JSON shape is owned by the parallel agent-intelligence ticket.

---

## Product and requirements assumptions

### ASS-001

- **Statement**: Hypothesis records are JSON files in the research directory, and this ticket reads that JSON without importing the agent-intelligence package.
- **Source**: User role for LOCAL-dataset-discovery; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: A hypothesis file is readable with no import of `agent_intelligence`.
- **Risk Level**: safe

### ASS-002

- **Statement**: The hypothesis id is the JSON field `id` or `hypothesisId`, and the measurement fields are `measurementFields` when that value is a list, otherwise `measurements` when that value is a list of strings.
- **Source**: Inferred from `requirements/LOCAL-agent-intelligence/functional.md` REQ-004 and the user role that names the hypothesis id
- **Verification**: A file using either id field and a list of measurement names is accepted, and prose measurements do not count as covered fields.
- **Risk Level**: risky
- **Mitigation**: Accept both id names and fail coverage closed when the measurements are prose.

### ASS-003

- **Statement**: A verification date is current when it is not after the judgment time and not more than 730 days before that time.
- **Source**: Inferred from `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` dataset suitability stage
- **Verification**: A date 731 days old is unsuitable and a date 730 days old is eligible on age.
- **Risk Level**: risky
- **Mitigation**: Keep 730 days as one named constant and cover both sides with tests.

### ASS-004

- **Statement**: The catalog search is supplied to the node, and this ticket does not require a live web-search credential.
- **Source**: `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 2
- **Verification**: A discovery run completes against an in-memory catalog with no network call.
- **Risk Level**: safe

### ASS-005

- **Statement**: An unsuitable judgment is stored so a later reader can see that the dataset was rejected for that hypothesis.
- **Source**: `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 1
- **Verification**: A failing candidate produces an entry whose suitability is `unsuitable`.
- **Risk Level**: safe

---

## Architecture assumptions

### ASS-ARCH-001

- **Statement**: Dataset discovery is one LangGraph node that uses a LangChain tool and stores JSON records.
- **Source**: `docs/adr/0001-langchain-langgraph.md`
- **Scope**: `dataset_discovery`
- **Risk Level**: safe
- **Impact if false**: The node, tool, and registry boundary would be rebuilt.

### ASS-ARCH-002

- **Statement**: Other agents are not called. They read `datasets.json` later.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Scope**: Handoff out of this ticket
- **Risk Level**: safe
- **Impact if false**: This ticket would start dataset validation.

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
| Product assumptions | 3 | 2 | 0 | 5 |
| Architecture assumptions | 2 | 0 | 0 | 2 |
| Open questions | - | - | - | 0 |

---

## Top priorities

| ID | Priority | Why it matters |
|----|----------|----------------|
| REQ-001 | critical | A suitable dataset must be stored with the name, source URL, title, suitability, and hypothesis id. |
| REQ-002 | critical | A query match or an incomplete dataset must not be recorded as suitable. |
| INV-002 | critical | Description match alone must never become a suitable registry entry. |
| POL-001 | critical | Any failed suitability check must record `unsuitable`. |
| REQ-004 | high | An unsuitable dataset must not be substituted as support for a hypothesis. |
| REQ-006 | high | Human text must not enter this agent. |
| INV-001 | high | A registry entry without identity fields cannot be traced to a hypothesis. |

---

## Autonomous handoff

- **Next stage**: planner
- **Proceed automatically**: yes
- **Planner input path**: requirements/LOCAL-dataset-discovery/
- **Reason if paused**: None
