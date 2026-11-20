# Constraints

---

## Technical constraints

### CON-005

- **Statement**: The evaluation result field is only PASS or REWORK.
- **Source**: User order for LOCAL-independent-evaluator
- **Scope**: evaluations.json

### CON-006

- **Statement**: LangChain with LangGraph is the accepted system framework, and this package follows the Python JSON-module style already applied in the repository.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; `research_orchestrator/`
- **Scope**: independent_evaluator package

## Architectural constraints

### Component and integration constraints

### CON-001

- **Statement**: Package independent_evaluator does not import research_orchestrator or any other component package.
- **Source**: User order for LOCAL-independent-evaluator
- **Scope**: independent_evaluator imports

### CON-003

- **Statement**: The evaluator does not send a message to another agent.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Scope**: independent_evaluator runtime

## Data constraints

### CON-007

- **Statement**: The evaluator's only written file is evaluations.json, and each object uses the fields hypothesis_id, stage, result, and trigger.
- **Source**: User order for LOCAL-independent-evaluator
- **Scope**: research record directory

## Performance and capacity constraints

None.

## Deployment and operational constraints

### CON-002

- **Statement**: The evaluator does not launch a shopping agent.
- **Source**: User order for LOCAL-independent-evaluator; `docs/adr/0001-langchain-langgraph.md`
- **Scope**: independent_evaluator runtime

### CON-004

- **Statement**: A faculty report is out of scope and is not written.
- **Source**: User order for LOCAL-independent-evaluator
- **Scope**: independent_evaluator outputs

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
