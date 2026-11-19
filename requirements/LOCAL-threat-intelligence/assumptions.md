# Assumptions

## Readiness

**Status**: READY_WITH_RISKS

**Work item ID**: LOCAL-threat-intelligence

**Base path**: requirements/LOCAL-threat-intelligence/

**Generated**: 2026-11-19 08:10 Europe/Dublin

**Analysis scope**: Capstone and agent-design specs under `docs/specs/`, plus user decisions on 2026-11-19 about scope, LangChain, the manual VM sandbox, the agent registry, and a system end-to-end test.

### Summary

Threat intelligence can be planned. It owns the assistant registry and human-facing addition reports, stores sourced shopping-session hypotheses, and excludes abuse classification. The system end-to-end test is in scope and depends on records from other agents plus a manual virtual-machine run. No blocking question remains.

### Blocking issues

None.

### Tracked risks

- CA-001: the end-to-end test stays red until the other stage records exist.
- Manual sandbox evidence varies with how a person runs the assistant on the VM.

---

## Product and requirements assumptions

### ASS-001

- **Statement**: The threat-intelligence agent owns the assistant registry and the addition reports.
- **Source**: User decision 2026-11-19, after this role was named as the researcher
- **Verification**: Registry writes occur only in this agent's stored records.
- **Risk Level**: safe
- **Mitigation**: None

### ASS-002

- **Statement**: A person runs Muse-like assistants on the sandbox VM, and this agent only reads the saved evidence.
- **Source**: User decision 2026-11-19
- **Verification**: An end-to-end run has a saved evidence file and no shopping-agent process started by this agent.
- **Risk Level**: safe
- **Mitigation**: None

### ASS-003

- **Statement**: Discovery may register an assistant that does not shop, and such an entry has a report and no shopping-session hypothesis.
- **Source**: User decision 2026-11-19 requiring emerging assistants in the registry; hypothesis rules in `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md`
- **Verification**: A discovered non-shopping assistant appears in the registry with a report and without a hypothesis.
- **Risk Level**: risky
- **Mitigation**: Keep hypothesis storage on POL-001 so registration does not invent a shopping signal.

---

## Architecture assumptions

### ASS-ARCH-001

- **Statement**: This agent is a LangGraph node that uses a LangChain ReAct loop and LangChain tools.
- **Source**: User decision 2026-11-19; `docs/adr/0001-langchain-langgraph.md`
- **Scope**: Threat-intelligence runtime
- **Risk Level**: safe
- **Impact if false**: Tool calling and the stage boundary would be rebuilt on another framework.

### ASS-ARCH-002

- **Statement**: Dataset validation, sandbox validation, the independent evaluator, and rule specification consume stored records and are not called directly by this agent.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` sections 3 and 5
- **Scope**: Downstream of hypothesis storage
- **Risk Level**: safe
- **Impact if false**: The one-way handoff and the end-to-end fixtures would change.

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
| Architecture assumptions | 2 | 0 | 0 | 2 |
| Open questions | - | - | - | 0 |

---

## Top priorities

| ID | Priority | Why it matters |
|----|----------|----------------|
| REQ-001 | critical | A human-named assistant must become a sourced registry entry. |
| REQ-003 | critical | Adding an assistant must be visible to a human. |
| REQ-004 | critical | A hypothesis without a signal, observation, sources, and measurements cannot be validated. |
| REQ-008 | critical | The system test is the acceptance check from research through a submitted rule specification. |
| INV-001 | critical | A hypothesis with no source must not enter the pipeline. |
| POL-001 | high | Weak sources must stop as an unresolved investigation. |
| POL-004 | high | The end-to-end test must not start a shopping agent. |

---

## Autonomous handoff

- **Next stage**: planner
- **Proceed automatically**: yes
- **Planner input path**: requirements/LOCAL-threat-intelligence/
- **Reason if paused**: None
