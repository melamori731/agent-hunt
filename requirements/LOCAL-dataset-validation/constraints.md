# Constraints

Limits and rules inferred from architecture diagrams, design documents, and source artifacts. Constraints are not requirements; they bound what solutions may do.

---

## Technical constraints

### CON-001

- **Statement**: Agent code uses LangChain tools and a LangGraph node, and this ticket does not reopen that framework choice.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user instruction not to revisit the ADR
- **Scope**: `dataset_validation` runtime

---

## Architectural constraints

### Component and integration constraints

### CON-002

- **Statement**: The package name is `dataset_validation`, and that package does not import another component package.
- **Source**: User scope for this ticket
- **Scope**: `dataset_validation` imports

### CON-003

- **Statement**: This ticket does not discover datasets, run the sandbox, or write a rule specification.
- **Source**: User scope for this ticket; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 3
- **Scope**: Dataset Validation responsibilities

---

## Data constraints

### CON-004

- **Statement**: The validation record is JSON in `dataset_results.json` and is not a faculty report.
- **Source**: User scope for JSON records and the faculty report
- **Scope**: Persistence

---

## Performance and capacity constraints

None. The coordination spec accepts high latency and does not set a latency target for this agent.

---

## Deployment and operational constraints

### CON-005

- **Statement**: This ticket does not deploy a detection rule and does not launch a shopping agent.
- **Source**: User scope for this ticket; `docs/adr/0001-langchain-langgraph.md` MVP sandbox consequence
- **Scope**: Runtime side effects

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Technical                | 1     |
| Architectural            | 2     |
| Data                     | 1     |
| Performance              | 0     |
| Deployment / operational | 1     |
| **Total**                | **5** |
