# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-independent-evaluator |
| **Requirements base path** | requirements/LOCAL-independent-evaluator/ |
| **Plan base path** | requirements/LOCAL-independent-evaluator/plan/ |
| **Plan** | [plan.md](./plan.md) |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |

## Status definitions

- `DECIDED`: selected for implementation and supported by sufficient evidence.
- `REQUIRES_ACK`: selected provisionally, but material risk requires human acknowledgement before implementation.
- `BLOCKED`: unresolved choice prevents safe implementation.
- `SUPERSEDED`: replaced by another decision; preserve the entry and link its replacement.

---

## Decision index

| ID | Decision | Status | Affected plan step(s) |
|----|----------|--------|-----------------------|
| DD-001 | One Python package appends evaluations.json and does not import other component packages | DECIDED | Step 1, Step 2, Step 3 |
| DD-002 | An evaluation result is only PASS or REWORK and never a workflow stage change | DECIDED | Step 2, Step 3 |
| DD-003 | Support paired with reject is the only validation contradiction | DECIDED | Step 3 |
| DD-004 | Input lists use local file and field names because sibling packages are not imported | REQUIRES_ACK | Step 3 |

---

## DD-001 — One Python package appends evaluations.json

- **Status**: DECIDED
- **Decision**: Package `independent_evaluator` uses the applied style of cohesive Python classes and JSON list files. It does not import `research_orchestrator` or another component package, and it does not add a LangGraph runtime in this ticket.
- **Scope**: Module boundary and dependency direction.
- **Rationale**: The code already in the repository stores records as JSON lists and does not import LangGraph. The ADR accepts LangChain and LangGraph for the system graph. This package is the check those nodes can call later. Adding a graph library here would depart from the applied modules.
- **Evidence**:
  - `research_orchestrator/store.py`
  - `docs/adr/0001-langchain-langgraph.md`
  - CON-001, CON-006, ASS-ARCH-001
- **Alternatives considered**:
  - **Import LangGraph and register a one-node graph** — the applied modules do not import it, and this ticket must not depend on other agents' runtimes.
  - **Import the orchestrator store** — the user forbade importing `research_orchestrator`.
- **Consequences**:
  - A later graph owner can call `IndependentEvaluator.evaluate` without this package owning stage transitions.
- **Affected plan steps**: Step 1, Step 2, Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — PASS or REWORK only, with no stage write

- **Status**: DECIDED
- **Decision**: `evaluations.json` stores hypothesis_id, stage, result, and trigger. Result is PASS or REWORK. The evaluator does not write ESCALATE, STOP, or any workflow stage file.
- **Scope**: Evaluation record and write set.
- **Rationale**: The user limited the result field to PASS or REWORK and assigned stage changes to the research orchestrator. The safety plan's ESCALATE and STOP decisions stay with that orchestrator.
- **Evidence**:
  - User order for LOCAL-independent-evaluator
  - INV-001, INV-002, CON-005, CON-007
  - `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` sections 5 and 7
- **Alternatives considered**:
  - **Store ESCALATE and STOP in evaluations.json** — the user limited result to PASS or REWORK.
  - **Update a stage file on REWORK** — that would write a workflow stage change.
- **Consequences**:
  - A contradiction becomes REWORK here. Suspension remains an orchestrator decision.
- **Affected plan steps**: Step 2, Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — Contradiction is support with reject

- **Status**: DECIDED
- **Decision**: Dataset and sandbox outcomes contradict only when one is support and the other is reject. Support with inconclusive, and support with blocked, do not contradict. A missing outcome is missing evidence, which is REWORK.
- **Scope**: Validation stage check.
- **Rationale**: The user requires a PASS only when the validation pair does not contradict. The orchestrator already treats support with inconclusive or blocked as not a contradiction, and support with an opposing reject as a contradiction. This package copies that meaning without importing the orchestrator.
- **Evidence**:
  - POL-002, REQ-003, REQ-004
  - `research_orchestrator/orchestrator.py` `review_validation`
  - User order for LOCAL-independent-evaluator
- **Alternatives considered**:
  - **Treat inconclusive as a contradiction** — that would reject a pair the orchestrator still considers consistent.
  - **Treat two rejects as a contradiction** — the two results agree.
- **Consequences**:
  - Callers that use a different outcome word receive REWORK because the expected outcome is absent.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — Local input file names

- **Status**: REQUIRES_ACK
- **Decision**: The evaluator reads `hypotheses.json`, `validations.json`, and `rule_specifications.json` from the directory it is given. It does not discover or import another package's store.
- **Scope**: Input contract.
- **Rationale**: The checks need stored records, and the import ban prevents sharing a store class. The names are fixed in this package so the checks are testable.
- **Evidence**:
  - ASS-002
  - CON-001
  - User order forbidding imports of other component packages
- **Alternatives considered**:
  - **Accept any file name that contains the fields** — a silent match would hide a bad record shape.
  - **Import `OrchestratorStore`** — forbidden by CON-001.
- **Consequences**:
  - A parallel writer that uses different names is judged as missing evidence and receives REWORK.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## Decision completeness

- [x] Every material architecture, boundary, dependency, contract, persistence, policy-placement, and consequential technology choice has a `DD-NNN` entry
- [x] Every active decision cites concrete evidence
- [x] Every active decision records alternatives and consequences
- [x] Every active decision maps to the plan step(s) it governs
- [x] Every `REQUIRES_ACK` decision is reflected in a `READY_FOR_IMPLEMENTATION_WITH_ACK` handoff
- [x] Every `BLOCKED` decision is reflected in a blocked handoff
- [x] Superseded decisions are preserved and linked to their replacements
