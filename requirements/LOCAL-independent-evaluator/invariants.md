# Invariants

---

## Data invariants

### INV-002

- **Statement**: Every stored evaluation contains hypothesis_id, stage, result, and a non-empty trigger, result is only PASS or REWORK, and the record contains no other field.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Verification**: Attempt to store an evaluation with an empty trigger, a result other than PASS or REWORK, or an extra field, and confirm the store rejects it.
- **If violated**: A later review cannot tell what was checked, or a stage change is smuggled into the evaluation file.

## Integrity invariants

### INV-001

- **Statement**: The evaluator writes evaluations.json and does not write or modify a workflow stage file.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` sections 5 and 7
- **Verification**: Place a stage file beside the records, run one PASS check and one REWORK check, and confirm the stage file bytes are unchanged.
- **If violated**: This package advances or rewrites a stage that only the research orchestrator may change.

## Business logic invariants

None.

## Security invariants

None.

## Consistency invariants

None.

---

## Summary

- **Total invariants**: 2
