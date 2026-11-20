# Constraints

---

## Technical constraints

### CON-001

- **Statement**: Dataset discovery is one LangGraph node that calls a LangChain tool and does not use a conversational multi-agent framework.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user decision 2026-11-20
- **Scope**: `dataset_discovery` runtime

## Architectural constraints

### CON-002

- **Statement**: Package `dataset_discovery` does not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, `sandbox_validation`, `detection_rule_specification`, or `independent_evaluator`.
- **Source**: User role for LOCAL-dataset-discovery
- **Scope**: Package imports

### CON-003

- **Statement**: Dataset discovery exchanges records with other agents only as stored JSON and does not chat with them.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5; user decision 2026-11-20
- **Scope**: Agent communication

### CON-008

- **Statement**: This ticket does not research shopping assistants and does not compute hypothesis validation metrics.
- **Source**: User decision 2026-11-20
- **Scope**: Discovery behavior

## Data constraints

### CON-004

- **Statement**: Dataset registry entries are stored in `datasets.json`.
- **Source**: User role for LOCAL-dataset-discovery
- **Scope**: Registry persistence

## Performance and capacity constraints

### CON-005

- **Statement**: Dataset discovery has no real-time completion deadline.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 6
- **Scope**: Discovery runs

## Deployment and operational constraints

### CON-006

- **Statement**: The faculty final report and presentation are out of scope for this work item.
- **Source**: User decision 2026-11-20; `docs/specs/DOCUMENT_TO_TASK_MAPPING.md`
- **Scope**: Deliverables of this ticket

### CON-007

- **Statement**: Production deployment of a detection rule is out of scope.
- **Source**: User decision 2026-11-20; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 5
- **Scope**: Rule outcome

### CON-009

- **Statement**: Detecting malicious or abusive agents is out of scope.
- **Source**: User decision 2026-11-20
- **Scope**: Research purpose

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Technical                | 1     |
| Architectural            | 3     |
| Data                     | 1     |
| Performance              | 1     |
| Deployment / operational | 3     |
| **Total**                | **9** |
