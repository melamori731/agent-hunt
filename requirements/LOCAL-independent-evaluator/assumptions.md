# Assumptions

## Readiness

**Status**: READY_WITH_RISKS

**Work item ID**: LOCAL-independent-evaluator

**Base path**: requirements/LOCAL-independent-evaluator/

**Generated**: 2026-11-20T18:28:00Z

**Analysis scope**: `docs/specs/Multi_Agent_Coordination_Capstone.md`, `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md`, `docs/adr/0001-langchain-langgraph.md`, and the user order for this ticket.

### Summary

The independent evaluator can be planned. It writes PASS or REWORK for one stored stage and does not change workflow stage. The tracked risk is the local JSON field names, because this package must not import the packages that write those records.

### Blocking issues

None.

### Tracked risks

ASS-002. Sibling packages implemented in parallel may store the same facts under different file or field names. Those records are REWORK until they match the names in this package.

---

## Product and requirements assumptions

### ASS-001

- **Statement**: Stage records and evaluations.json are JSON lists in one directory supplied to the evaluator.
- **Source**: `research_orchestrator/store.py`; user order naming evaluations.json
- **Verification**: Write a list file, run one check, and read the evaluation list back
- **Risk Level**: safe

### ASS-002

- **Statement**: The hypothesis list is hypotheses.json, the validation list is validations.json, and the rule specification list is rule_specifications.json, using hypothesis_id, sources, kind, outcome, submitted, deployed, research_sources, and validation_results.
- **Source**: inferred, because the user forbade importing the writer packages
- **Verification**: A record that uses these names is judged by REQ-001, REQ-003, and REQ-005
- **Risk Level**: risky
- **Mitigation**: Keep the names in one class and treat any other shape as missing evidence, which writes REWORK

### ASS-003

- **Statement**: A source, research source, or validation result counts when it is a non-empty string or an object with a non-empty url or title.
- **Source**: inferred from "has sources" and "cites research sources and validation results"
- **Verification**: An empty string fails the check and a title-only object passes it
- **Risk Level**: safe

---

## Architecture assumptions

### ASS-ARCH-001

- **Statement**: The evaluator is one Python package that appends JSON records and does not import a graph runtime in this ticket.
- **Source**: `research_orchestrator/`; `docs/adr/0001-langchain-langgraph.md`
- **Scope**: independent_evaluator
- **Risk Level**: safe
- **Impact if false**: The check would need a LangGraph node wrapper before the orchestrator could call it as a graph step.

### ASS-ARCH-002

- **Statement**: PASS and REWORK are the only results this package stores. ESCALATE and STOP remain orchestrator decisions and are not evaluation results.
- **Source**: User order limiting result to PASS or REWORK; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Scope**: evaluations.json
- **Risk Level**: safe
- **Impact if false**: The orchestrator would not be the sole writer of suspension and termination.

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
| REQ-001 | critical | A hypothesis without sources must not pass. |
| REQ-003 | critical | A consistent validation pair is the only validation PASS. |
| REQ-005 | critical | A rule passes only when it is submitted, not deployed, and cited. |
| REQ-002 | critical | Missing hypothesis evidence is REWORK and is not a stage change. |
| INV-001 | critical | This package must not write workflow stage changes. |
| POL-003 | high | The rule check is the gate before human review. |

---

## Autonomous handoff

- **Next stage**: planner
- **Proceed automatically**: yes
- **Planner input path**: requirements/LOCAL-independent-evaluator/
- **Reason if paused**: None
