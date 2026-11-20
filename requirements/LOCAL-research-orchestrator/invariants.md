# Invariants

---

## Data invariants

### INV-002

- **Statement**: Every PASS, REWORK, ESCALATE, and STOP record contains both the trigger and the decision.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Verification**: Attempt to store a decision without a trigger and confirm the store rejects it.
- **If violated**: A later review cannot tell why the workflow moved.

## Integrity invariants

### INV-001

- **Statement**: Workflow stage changes are written only by the research orchestrator.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 5
- **Verification**: Run one standup and confirm stage records name the orchestrator as the writer.
- **If violated**: Another agent can skip a gate.

## Business logic invariants

None.

## Security invariants

### INV-003

- **Statement**: The orchestrator does not write a deployed detection rule.
- **Source**: User decision 2026-11-19
- **Verification**: Finish a standup that requests a rule specification and confirm no deployed-rule record exists.
- **If violated**: An unreviewed rule is treated as active.

## Consistency invariants

None.

---

## Summary

- **Total invariants**: 3
