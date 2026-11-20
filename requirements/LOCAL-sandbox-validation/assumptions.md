# Assumptions

## Readiness

**Status**: READY_WITH_RISKS

**Work item ID**: LOCAL-sandbox-validation

**Base path**: requirements/LOCAL-sandbox-validation/

**Generated**: 2026-11-20T18:28:00Z

**Analysis scope**: `docs/specs/Multi_Agent_Coordination_Capstone.md`, the sandbox loop in `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md`, `docs/adr/0001-langchain-langgraph.md`, and the user decisions for LOCAL-sandbox-validation.

### Summary

Sandbox validation reads a hypothesis and a saved evidence file and writes `sandbox_results.json`. Muse-like agents stay manual. The evidence JSON shape and the provisional four-of-five rule are tracked risks, not blockers.

### Blocking issues

None.

### Tracked risks

- ASS-002: a saved evidence file is judged only when it is a JSON object with `runs` of `telemetry_present` and `signal_observed`.
- The capstone line that sandbox validation executes agents is settled by the ADR and the user: this package does not launch those agents.

---

## Product and requirements assumptions

### ASS-001

- **Statement**: The sandbox is a self-hosted shopping page on a virtual machine, and a person runs Muse-like agents there.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user decision 2026-11-20
- **Verification**: This package has no launcher for Muse, browser-use, WebArena, or a shopping agent.
- **Risk Level**: safe

### ASS-002

- **Statement**: Saved evidence is a JSON object whose `runs` array records `telemetry_present` and `signal_observed` for each manual run.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` sandbox steps 3–6; user decision that the package loads a saved evidence JSON file
- **Verification**: A file with that shape yields support, contradict, or inconclusive; any other shape yields blocked.
- **Risk Level**: risky
- **Mitigation**: Unreadable or incomplete evidence is blocked and is not replaced with a guessed observation.

---

## Architecture assumptions

### ASS-ARCH-001

- **Statement**: Sandbox validation is one LangGraph node in package `sandbox_validation` that calls a LangChain runnable to load files.
- **Source**: `docs/adr/0001-langchain-langgraph.md`
- **Scope**: `sandbox_validation`
- **Risk Level**: safe
- **Impact if false**: The node would not match the accepted workflow framework.

### ASS-ARCH-002

- **Statement**: This package does not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, or `rule_specification`.
- **Source**: User decision 2026-11-20
- **Scope**: `sandbox_validation`
- **Risk Level**: safe
- **Impact if false**: Sandbox validation would take on another component's work.

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
| Product assumptions | 1 | 1 | 0 | 2 |
| Architecture assumptions | 2 | 0 | 0 | 2 |
| Open questions | - | - | - | 0 |

---

## Top priorities

| ID | Priority | Why it matters |
|----|----------|----------------|
| REQ-001 | critical | The only output is `sandbox_results.json` with `hypothesis_id`, `result`, and `evidence_path`. |
| REQ-002 | critical | Missing evidence is blocked and must not start a browser or shopping agent. |
| INV-001 | critical | The package must not import `subprocess` or start a process. |
| POL-001 | critical | Evidence that cannot be read or has no telemetry is blocked. |
| POL-002 | high | Support, contradict, and inconclusive come from the saved-run rule. |

---

## Autonomous handoff

- **Next stage**: planner
- **Proceed automatically**: yes
- **Planner input path**: requirements/LOCAL-sandbox-validation/
- **Reason if paused**: None
