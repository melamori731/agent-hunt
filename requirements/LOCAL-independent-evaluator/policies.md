# Policies

---

## Business decision policies

### POL-001

- **Statement**: When the requested stage is hypothesis, the evaluator writes PASS only if the stored hypothesis contains at least one source, and otherwise writes REWORK.
- **Source**: User order for LOCAL-independent-evaluator
- **Verification**: Compare one sourced hypothesis with one empty source list and confirm only the sourced hypothesis is PASS.
- **Related requirements**: REQ-001, REQ-002

### POL-002

- **Statement**: When the requested stage is validation, the evaluator writes PASS only if both the dataset outcome and the sandbox outcome are present and the pair is not support with reject, and otherwise writes REWORK.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 1
- **Verification**: Confirm support with inconclusive is PASS and support with reject is REWORK.
- **Related requirements**: REQ-003, REQ-004

### POL-003

- **Statement**: When the requested stage is rule_specification, the evaluator writes PASS only if the specification is submitted, is not deployed, and cites at least one research source and at least one validation result, and otherwise writes REWORK.
- **Source**: User order for LOCAL-independent-evaluator; `docs/adr/0001-langchain-langgraph.md`
- **Verification**: Confirm one complete submitted specification is PASS and one deployed specification is REWORK.
- **Related requirements**: REQ-005, REQ-006

## Operational decision policies

None.

## Routing and classification policies

### POL-004

- **Statement**: When a stored record for the hypothesis id is an abuse classification, the evaluator writes REWORK with a trigger that does not name an abuse, malicious, or legitimate label, and it does not start a process or write an agent message.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: Store a hypothesis whose purpose is abuse classification and confirm the evaluation result is REWORK, the trigger contains none of those labels, and no message file or process launch occurs.
- **Related requirements**: REQ-007

## Data handling policies

None.

## Security behavior policies

None.

## Fallback and exception policies

None.

## User experience policies

None.

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Business decision        | 3     |
| Operational decision     | 0     |
| Routing / classification | 1     |
| Data handling            | 0     |
| Security behavior        | 0     |
| Fallback / exception     | 0     |
| User experience          | 0     |
| **Total**                | **4** |
