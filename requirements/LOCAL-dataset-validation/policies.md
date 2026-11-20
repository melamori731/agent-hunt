# Policies

Software architecture policies: one condition and one resulting system behavior.

---

## Business decision policies

### POL-002

- **Statement**: When both class rates are numbers, the agent stores support if prevalence is strictly greater than the false-positive rate, contradict if prevalence is strictly less, and inconclusive if the two rates are equal.
- **Source**: ASS-002; user definitions of support, contradict, and inconclusive
- **Verification**: Pass a higher AI rate, a higher human rate, and equal rates into the deciding class and read the three results.
- **Related requirements**: REQ-001, REQ-002, REQ-003

---

## Operational decision policies

### POL-003

- **Statement**: When the payload does not carry `source` orchestrator together with `hypothesis_id`, `signal`, and `dataset_path`, the agent stores no dataset result.
- **Source**: User scope that human input arrives only through the orchestrator
- **Verification**: Submit a chat payload that lacks those fields and confirm no record is appended.
- **Related requirements**: REQ-006

---

## Routing and classification policies

None.

## Data handling policies

### POL-001

- **Statement**: When the named dataset file is missing, the agent stores blocked with null prevalence and a null false-positive rate and does not invent rows.
- **Source**: User scope that blocked means the dataset is missing; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` Dataset Validation step 3
- **Verification**: Resolve a missing path and read one blocked record whose rates are null.
- **Related requirements**: REQ-004

---

## Security behavior policies

None.

## Fallback and exception policies

### POL-004

- **Statement**: When the assignment asks to discover a dataset, launch a shopping agent, write a rule, or classify abuse, the agent stores no dataset result and does not perform that action.
- **Source**: User settled scope; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: Submit each forbidden action and confirm the result file is unchanged.
- **Related requirements**: REQ-005

---

## User experience policies

None.

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Business decision        | 1     |
| Operational decision     | 1     |
| Routing / classification | 0     |
| Data handling            | 1     |
| Security behavior        | 0     |
| Fallback / exception     | 1     |
| User experience          | 0     |
| **Total**                | **4** |
