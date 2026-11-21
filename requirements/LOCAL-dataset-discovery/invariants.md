# Invariants

---

## Data invariants

### INV-001

- **Statement**: Every stored registry entry has a non-empty dataset name, an http or https source URL, a non-empty title, a suitability of `suitable` or `unsuitable`, and a non-empty hypothesis id.
- **Source**: User role for LOCAL-dataset-discovery
- **Verification**: Attempt to store an entry that omits each of those fields and confirm each attempt is rejected.
- **If violated**: Validation would receive a dataset it cannot identify or trace.

## Integrity invariants

### INV-002

- **Statement**: A candidate whose only match is the search query is never stored with suitability `suitable`.
- **Source**: `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 1
- **Verification**: Judge one query-only candidate that otherwise looks complete and confirm suitability is `unsuitable`.
- **If violated**: A description match would be treated as a dataset that could support a hypothesis.

## Business logic invariants

## Security invariants

### INV-003

- **Statement**: Dataset discovery does not start a shopping-agent process.
- **Source**: User decision 2026-11-20; `docs/adr/0001-langchain-langgraph.md`
- **Verification**: Run discovery and confirm no shopping-agent process is started.
- **If violated**: The sandbox would run an agent this ticket must not launch.

## Consistency invariants

---

## Summary

- **Total invariants**: 3
