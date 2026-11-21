# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-research-orchestrator |
| **Requirements base path** | requirements/LOCAL-research-orchestrator/ |
| **Plan base path** | requirements/LOCAL-research-orchestrator/plan/ |
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
| DD-001 | One LangGraph node writes assignment records | DECIDED | Step 3 |
| DD-002 | JSON files store assignments and stage decisions | DECIDED | Step 4 |
| DD-003 | Human input becomes an agent-intelligence assignment | DECIDED | Step 3 |
| DD-004 | Standup interval defaults to 24 hours | DECIDED | Step 5 |
| DD-005 | Rework limit defaults to 2 | DECIDED | Step 2 |
| DD-006 | A submitted specification is stored and not deployed | DECIDED | Step 3 |
| DD-007 | Waiting hypotheses are assigned to both validators | DECIDED | Step 3 |

---

## DD-001 — One LangGraph node writes assignment records

- **Status**: DECIDED
- **Decision**: The research orchestrator is one LangGraph node. It stores assignment and decision records. It does not message other agents.
- **Scope**: Orchestrator runtime.
- **Rationale**: The accepted framework is LangGraph, and the coordination spec forbids direct agent dialogue.
- **Evidence**:
  - CON-001, CON-002, ASS-ARCH-001
  - `docs/adr/0001-langchain-langgraph.md`
  - `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Alternatives considered**:
  - **CrewAI manager chat** — that is the dialogue the coordination spec excludes.
- **Consequences**:
  - Other agents read stored assignments. This ticket does not run them.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — JSON files store assignments and stage decisions

- **Status**: DECIDED
- **Decision**: Assignments, stage decisions, and submitted specifications are JSON files in the same research store shape used by agent intelligence.
- **Scope**: Persistence.
- **Rationale**: Standup output must survive the process, and a separate database is not required for the MVP.
- **Evidence**:
  - QR-002, CON-004
  - `requirements/LOCAL-agent-intelligence/plan/design-decisions.md` DD-002
- **Alternatives considered**:
  - **SQLite** — more query power than this ticket's record reads need.
- **Consequences**:
  - Agent intelligence and the orchestrator can read the same directory layout.
- **Affected plan steps**: Step 4
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — Human input becomes an agent-intelligence assignment

- **Status**: DECIDED
- **Decision**: A human assistant name is stored as one assignment for agent intelligence. The orchestrator does not search or write a hypothesis.
- **Scope**: Human entry.
- **Rationale**: The user placed human input on the orchestrator, and the coordination spec gives research to the intelligence role.
- **Evidence**:
  - REQ-001, ASS-001
  - User decision 2026-11-19
- **Alternatives considered**:
  - **The orchestrator runs ReAct research** — that duplicates agent intelligence.
- **Consequences**:
  - Abuse-only requests create no assignment.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — Standup interval defaults to 24 hours

- **Status**: DECIDED
- **Decision**: The standup interval is configured. When no value is set, it is 24 hours.
- **Scope**: Standup schedule.
- **Rationale**: The sources require a scheduled standup and state no period. Agent intelligence discovery already defaults to 24 hours, and standups have no real-time deadline.
- **Evidence**:
  - REQ-003, CA-002, CON-005
  - `requirements/LOCAL-agent-intelligence/` REQ-010
- **Alternatives considered**:
  - **No default** — an unset interval would never start a standup.
  - **Hourly** — the spec accepts high latency and does not ask for a tighter loop.
- **Consequences**:
  - Tests can set the interval to 1 hour. Operators can change the default.
- **Affected plan steps**: Step 5
- **Supersedes**: None
- **Superseded by**: None

---

## DD-005 — Rework limit defaults to 2

- **Status**: DECIDED
- **Decision**: The rework limit is configured. When no value is set, it is 2. The next correctable failure at that count is ESCALATE.
- **Scope**: REWORK handling.
- **Rationale**: The safety plan requires a finite limit and gives no number. Two returns allow one correction and one confirmation before a human is required.
- **Evidence**:
  - REQ-008, POL-002, POL-003, CA-002
  - `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Alternatives considered**:
  - **Unlimited rework** — the safety plan forbids it.
  - **Limit of 1** — a single failure would always reach a human.
- **Consequences**:
  - Tests set the limit explicitly. The default is replaceable configuration.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-006 — A submitted specification is stored and not deployed

- **Status**: DECIDED
- **Decision**: An eligible hypothesis produces a stored rule-specification request and, when that specification exists, a human-review record. The orchestrator writes no deployed rule.
- **Scope**: Rule outcome.
- **Rationale**: The user ended the system at a submitted specification. The safety diagram's deployment step is out of scope.
- **Evidence**:
  - REQ-007, INV-003, CON-007
  - User decision 2026-11-19
- **Alternatives considered**:
  - **Follow the safety diagram through production deployment** — the user excluded that outcome.
- **Consequences**:
  - Human review here records the submission. It does not activate a detector.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-007 — Waiting hypotheses are assigned to both validators

- **Status**: DECIDED
- **Decision**: One hypothesis awaiting validation produces two assignment records: dataset validation and sandbox validation. Sandbox assignment points at the manual virtual-machine evidence flow and does not start a shopping agent.
- **Scope**: Validation routing.
- **Rationale**: The coordination diagram sends hypotheses to both validators, and sandbox execution stays manual.
- **Evidence**:
  - REQ-003, CON-003
  - `docs/specs/Multi_Agent_Coordination_Capstone.md` section 1
- **Alternatives considered**:
  - **Assign only one validator** — that drops the parallel check the diagram requires.
- **Consequences**:
  - A missing sandbox run stays a blocked or inconclusive record supplied later. This ticket does not invent the run.
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
