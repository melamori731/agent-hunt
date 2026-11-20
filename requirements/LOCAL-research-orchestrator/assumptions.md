# Assumptions

## Readiness

**Status**: READY_WITH_RISKS

**Work item ID**: LOCAL-research-orchestrator

**Base path**: requirements/LOCAL-research-orchestrator/

**Generated**: 2026-11-20 17:20 Europe/Dublin

**Analysis scope**: Coordination, reasoning-loop, and safety specs under `docs/specs/`, the accepted LangChain decision, and the user decisions on human input, manual sandbox runs, abuse scope, and submitted rule specifications.

### Summary

The research orchestrator can be planned. It accepts human assistant names, runs standups, writes assignments, and stops at a submitted specification. Abuse classification is refused. Deployment is out of scope. The standup interval and the rework limit are configured values. No blocking question remains.

### Blocking issues

None.

### Tracked risks

- CA-001: validator and rule-specification agents are not part of this ticket.
- CA-002: the standup interval and the rework limit have no number in the source documents.

---

## Product and requirements assumptions

### ASS-001

- **Statement**: A human assistant name is the human input this orchestrator accepts for research.
- **Source**: User decision 2026-11-19
- **Verification**: One submitted name produces one agent-intelligence assignment.
- **Risk Level**: safe
- **Mitigation**: None

### ASS-002

- **Statement**: Agent intelligence continues to start its own discovery run and does not wait for a standup to do that discovery.
- **Source**: `requirements/LOCAL-agent-intelligence/` REQ-010
- **Verification**: A discovery run can start with no new standup assignment.
- **Risk Level**: safe
- **Mitigation**: None

---

## Architecture assumptions

### ASS-ARCH-001

- **Statement**: This orchestrator is a LangGraph node that writes JSON assignment and decision records.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user decision 2026-11-19
- **Scope**: Orchestrator runtime and records
- **Risk Level**: safe
- **Impact if false**: Assignment handoff and the stage graph would be rebuilt.

### ASS-ARCH-002

- **Statement**: The independent evaluator is a separate role. This ticket reads its result and does not implement the evaluator.
- **Source**: User decision 2026-11-19; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 5
- **Scope**: Stage advance
- **Risk Level**: safe
- **Impact if false**: REQ-006 would move into this ticket.

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
| Product assumptions | 2 | 0 | 0 | 2 |
| Architecture assumptions | 2 | 0 | 0 | 2 |
| Open questions | - | - | - | 0 |

---

## Top priorities

| ID | Priority | Why it matters |
|----|----------|----------------|
| REQ-001 | critical | Human input must become an agent-intelligence assignment and must not be researched here. |
| REQ-003 | critical | Waiting hypotheses must be assigned to both validators. |
| REQ-004 | critical | One supporting result can request a rule specification only with lower confidence. |
| REQ-007 | critical | The outcome is a submitted specification, not a deployed rule. |
| INV-001 | critical | Only the orchestrator may change workflow stage. |
| POL-003 | high | Contradictions and exhausted rework must stop for a human. |
| REQ-008 | high | Rework must be finite. |

---

## Autonomous handoff

- **Next stage**: planner
- **Proceed automatically**: yes
- **Planner input path**: requirements/LOCAL-research-orchestrator/
- **Reason if paused**: None
