# Constraints

Limits and rules inferred from architecture diagrams, design documents, and source artifacts. Constraints are not requirements; they bound what solutions may do.

---

## Technical constraints

### CON-001

- **Statement**: Package `sandbox_validation` must not import `subprocess` or start a process.
- **Source**: User decision 2026-11-20
- **Scope**: `sandbox_validation`

### CON-002

- **Statement**: The workflow framework is LangChain plus LangGraph.
- **Source**: `docs/adr/0001-langchain-langgraph.md`
- **Scope**: `sandbox_validation`

## Architectural constraints

### Component and integration constraints

### CON-003

- **Statement**: `sandbox_validation` must not import another component package.
- **Source**: User decision 2026-11-20
- **Scope**: `sandbox_validation`

### CON-004

- **Statement**: This package must not chat with another agent.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5; user decision 2026-11-20
- **Scope**: `sandbox_validation`

## Data constraints

### CON-005

- **Statement**: The result file is `sandbox_results.json` and its fields are `hypothesis_id`, `result`, and `evidence_path`.
- **Source**: User decision 2026-11-20
- **Scope**: `sandbox_results.json`

## Performance and capacity constraints

None. The coordination spec accepts high latency.

## Deployment and operational constraints

### CON-006

- **Statement**: This package must not launch Muse, browser-use, WebArena, or any shopping agent.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user decision 2026-11-20
- **Scope**: `sandbox_validation`

### CON-007

- **Statement**: A faculty report is out of scope.
- **Source**: User decision 2026-11-20
- **Scope**: `sandbox_validation`

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Technical                | 2     |
| Architectural            | 2     |
| Data                     | 1     |
| Performance              | 0     |
| Deployment / operational | 2     |
| **Total**                | **7** |
