# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-dataset-validation |
| **Requirements base path** | requirements/LOCAL-dataset-validation/ |
| **Plan base path** | requirements/LOCAL-dataset-validation/plan/ |
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
| DD-001 | One LangGraph node calls one LangChain counting tool | DECIDED | Step 1, Step 4 |
| DD-002 | Results are appended to `dataset_results.json` | DECIDED | Step 3 |
| DD-003 | Support, contradict, and inconclusive follow a strict rate comparison | REQUIRES_ACK | Step 2 |
| DD-004 | `dataset_validation` does not import other component packages | DECIDED | Step 1 |
| DD-005 | Only an orchestrator assignment may store a result | DECIDED | Step 4 |

---

## DD-001 — One LangGraph node calls one LangChain counting tool

- **Status**: DECIDED
- **Decision**: `DatasetValidationGraph` is one LangGraph node. The node calls the LangChain tool `count_labelled_signal` to count AI and human rows. The node does not call a chat model.
- **Scope**: Runtime entry of `dataset_validation`.
- **Rationale**: The accepted ADR selects LangChain tools and LangGraph nodes, and the user said not to reopen that choice.
- **Evidence**:
  - CON-001, ASS-ARCH-001
  - `docs/adr/0001-langchain-langgraph.md`
  - Architecture validator for `LangChain with LangGraph`: confidence high, conflicts empty, recommendation proceed
- **Alternatives considered**:
  - **Plain functions only, matching the current `research_orchestrator` modules** — that module does not import LangGraph, and using only that pattern would reopen the ADR.
- **Consequences**:
  - This package depends on LangChain and LangGraph. It still stores JSON and does not import `research_orchestrator`.
- **Affected plan steps**: Step 1, Step 4
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — Results are appended to `dataset_results.json`

- **Status**: DECIDED
- **Decision**: `DatasetResultStore` appends each result to `dataset_results.json`. Each object has `hypothesis_id`, `result`, `prevalence`, `false_positive_rate`, and `dataset_name`.
- **Scope**: Persistence.
- **Rationale**: The user named that file and those fields, and the orchestrator already persists JSON lists on disk.
- **Evidence**:
  - REQ-007, QR-002, CON-004
  - `research_orchestrator/store.py`
- **Alternatives considered**:
  - **SQLite** — the orchestrator store is a JSON list, and this ticket does not need a query engine.
- **Consequences**:
  - A later reader opens the same file. This package does not import the orchestrator store.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — Support, contradict, and inconclusive follow a strict rate comparison

- **Status**: REQUIRES_ACK
- **Decision**: `DatasetResultRecord` stores support when AI prevalence is strictly greater than the human false-positive rate, contradict when it is strictly less, and inconclusive when the two rates are equal or cannot be computed. Blocked is only the missing file, with both rates null.
- **Scope**: Result selection.
- **Rationale**: The user defined four exclusive results and did not give a numeric cutoff. A strict comparison is the smallest rule that uses both measured rates.
- **Evidence**:
  - ASS-002, POL-002, INV-002, REQ-001, REQ-002, REQ-003, REQ-004
- **Alternatives considered**:
  - **Support whenever prevalence is greater than zero** — a signal that is more common in human rows would still be support, which contradicts the refute definition.
  - **A fixed false-positive ceiling such as 0.05** — no source states that ceiling.
- **Consequences**:
  - Equal rates do not count as support. The acknowledgement reason records this comparison.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — `dataset_validation` does not import other component packages

- **Status**: DECIDED
- **Decision**: The package reads the assignment and the fixture path. It does not import `research_orchestrator`, `agent_intelligence`, sandbox, dataset discovery, or rule specification.
- **Scope**: Package boundary.
- **Rationale**: The user forbade imports of other component packages, and the orchestrator boundary test already treats `dataset_validation` as a separate package.
- **Evidence**:
  - CON-002, CON-003, ASS-003
  - `tests/test_boundary.py`
- **Alternatives considered**:
  - **Import the orchestrator store** — that couples this package to another component.
- **Consequences**:
  - Hypothesis fields arrive on the assignment. A field-name mismatch with another package is outside this ticket.
- **Affected plan steps**: Step 1
- **Supersedes**: None
- **Superseded by**: None

---

## DD-005 — Only an orchestrator assignment may store a result

- **Status**: DECIDED
- **Decision**: The graph stores a result only when `source` is `orchestrator` and the payload includes `hypothesis_id`, `signal`, and `dataset_path`. A chat payload or a request to discover a dataset, launch a shopping agent, write a rule, or classify abuse stores nothing.
- **Scope**: Input gate on `DatasetValidationGraph`.
- **Rationale**: Human input reaches this agent only through the orchestrator, and the settled scope excludes those other actions.
- **Evidence**:
  - REQ-005, REQ-006, POL-003, POL-004, CON-005
  - `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Alternatives considered**:
  - **Accept any JSON object that names a file** — that would let a human chat path store a result.
- **Consequences**:
  - The orchestrator must set `source` to `orchestrator` on the assignment it hands this agent.
- **Affected plan steps**: Step 4
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
