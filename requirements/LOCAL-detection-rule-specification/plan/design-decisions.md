# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-detection-rule-specification |
| **Requirements base path** | requirements/LOCAL-detection-rule-specification/ |
| **Plan base path** | requirements/LOCAL-detection-rule-specification/plan/ |
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
| DD-001 | One LangGraph node calls one LangChain tool | DECIDED | Step 5 |
| DD-002 | JSON files are the read and write contract | REQUIRES_ACK | Step 4, Step 5 |
| DD-003 | This package imports no other component | DECIDED | Step 1 |
| DD-004 | Result vocabulary matches the stored validation words | DECIDED | Step 3 |
| DD-005 | The template has two evidence sections | DECIDED | Step 2 |
| DD-006 | A repeat write keeps one record per hypothesis | DECIDED | Step 4 |

---

## DD-001 — One LangGraph node calls one LangChain tool

- **Status**: DECIDED
- **Decision**: `DetectionRuleSpecification` is one LangGraph node named `specify`. That node calls the LangChain tool `assemble_rule_specification`. The package does not add a second framework.
- **Scope**: Runtime of this component.
- **Rationale**: ADR 0001 selects LangChain and LangGraph. This component does not research, so the tool assembles a record from stored evidence instead of running a search loop.
- **Evidence**:
  - CON-001, ASS-ARCH-001
  - `docs/adr/0001-langchain-langgraph.md`
  - User instruction 2026-11-20
- **Alternatives considered**:
  - **A plain Python function with no graph** — the research orchestrator package is written that way, and it would drop the accepted framework for this node.
  - **A ReAct search loop** — this component does not retrieve publications.
- **Consequences**:
  - Tests compile a LangGraph graph and invoke the LangChain tool.
  - The orchestrator package stays unchanged.
- **Affected plan steps**: Step 5
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — JSON files are the read and write contract

- **Status**: REQUIRES_ACK
- **Decision**: The store directory holds `hypotheses.json`, `validation_results.json`, and `rule_specifications.json`. A hypothesis id is read from `hypothesis_id` or, when that key is absent, from `id`. Research sources are read from `research_sources` or, when that key is absent, from `sources`. Validation results are read from `dataset_result` and `sandbox_result`, including when those keys sit under `validation_results`.
- **Scope**: Persistence.
- **Rationale**: The user required `rule_specifications.json` and forbade imports of other component packages. Sibling writers are not in this package, and the orchestrator already uses `id` on hypothesis dicts plus the words support, inconclusive, blocked, and contradict.
- **Evidence**:
  - ASS-003, CA-001, REQ-004, CON-002
  - User settled scope 2026-11-20
  - `research_orchestrator/orchestrator.py` `review_validation`
- **Alternatives considered**:
  - **Import `research_orchestrator`** — the user forbade imports of other component packages.
  - **A database** — the applied store in this repo is JSON files.
- **Consequences**:
  - Tests fixture these file names.
  - A sibling writer that uses a different file name will not be seen until the contract is aligned. That is the acknowledgement reason.
- **Affected plan steps**: Step 4, Step 5
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — This package imports no other component

- **Status**: DECIDED
- **Decision**: `detection_rule_specification` does not import `research_orchestrator`, `agent_intelligence`, dataset validation, dataset discovery, sandbox validation, or a shopping-agent launcher, and it does not spawn a subprocess.
- **Scope**: Package boundary.
- **Rationale**: The user limited this component to reading stored records and writing the specification.
- **Evidence**:
  - CON-002, CON-003, CON-005, REQ-004, POL-001
  - User settled scope 2026-11-20
- **Alternatives considered**:
  - **Call the orchestrator to decide eligibility** — that imports another component and moves this decision out of the specification package.
- **Consequences**:
  - A structural test scans the package source for those imports.
- **Affected plan steps**: Step 1
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — Result vocabulary matches the stored validation words

- **Status**: DECIDED
- **Decision**: `EvidenceConfidence` returns `standard` when both results are `support` and sources are complete. It returns `lower` when one result is `support` and the other is `inconclusive` or `blocked`. It returns no specification when either result is `contradict`, a source is missing, or a result is absent or unrecognized.
- **Scope**: Eligibility and confidence.
- **Rationale**: Those four result words are already stored by the orchestrator review path, and the user defined standard versus lower confidence and the refusal cases.
- **Evidence**:
  - REQ-001, REQ-002, REQ-003, ASS-002
  - User settled scope 2026-11-20
  - `research_orchestrator/orchestrator.py`
- **Alternatives considered**:
  - **Treat a missing validation file as inconclusive** — the user allowed lower confidence only for inconclusive or blocked, not for a missing result.
  - **Add numeric confidence** — the user named two labels, standard and lower.
- **Consequences**:
  - Unrecognized result strings produce no specification.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-005 — The template has two evidence sections

- **Status**: DECIDED
- **Decision**: `SpecificationTemplate` sections are `research_sources` and `validation_results`. Each source has `url` and `title`. Validation results have `dataset_result` and `sandbox_result`. The record also has `hypothesis_id`, `submitted` true, `deployed` false, and `confidence`. It has no abuse or legitimacy field.
- **Scope**: Specification document.
- **Rationale**: The user defined the specification evidence as research sources plus validation results and required those record fields.
- **Evidence**:
  - REQ-001, INV-001, INV-002, INV-003
  - User settled scope 2026-11-20
- **Alternatives considered**:
  - **Add telemetry thresholds from the earlier generate-critique-revise note** — the settled scope limits the template to the two evidence sections.
- **Consequences**:
  - The template rejects a record outside that shape.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-006 — A repeat write keeps one record per hypothesis

- **Status**: DECIDED
- **Decision**: Saving a specification replaces any existing `rule_specifications.json` row with the same `hypothesis_id`. Two runs on the same inputs leave equal file contents.
- **Scope**: Specification persistence.
- **Rationale**: QR-001 requires equal records for the same stored inputs, and a second append would change the file.
- **Evidence**:
  - QR-001, QR-002
- **Alternatives considered**:
  - **Append a new row on every run** — the file would grow and the two runs would not leave the same records.
- **Consequences**:
  - One hypothesis has one current specification in the file.
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
