# Invariants

Stable truths the system must never violate. Requirements and designs must not contradict these.

---

## Data invariants

#### INV-002

- **Statement**: `sandbox_results.json` contains only `hypothesis_id`, `result`, and `evidence_path`.
- **Source**: User decision 2026-11-20
- **Verification**: Read the written file and confirm the key set is exactly those three names.
- **If violated**: A later stage can treat an abuse label or a deployed rule as a sandbox result.

## Integrity invariants

None.

## Business logic invariants

None.

## Security invariants

#### INV-001

- **Statement**: Package `sandbox_validation` does not import `subprocess` and a validation run does not start a process.
- **Source**: User decision 2026-11-20; `docs/adr/0001-langchain-langgraph.md`
- **Verification**: Parse the package and fail the unit test when `subprocess` is imported or a validation run starts a process.
- **If violated**: The package would launch a browser or a shopping agent.

## Consistency invariants

None.

---

## Summary

- **Total invariants**: 2
