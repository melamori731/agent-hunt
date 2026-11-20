# Quality Requirements

Non-functional and quality attributes.

---

## Performance

None. No latency target is stated for this agent.

## Reliability

### QR-001

- **Statement**: On a support, contradict, or equal-rate inconclusive record, `prevalence` equals the count of AI rows where the signal is true divided by the count of AI rows, and `false_positive_rate` equals the count of human rows where the signal is true divided by the count of human rows.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` external tools; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` false-positive rate formula
- **Verification**: Use fixtures with known class counts and compare both stored rates with those ratios.
- **Dependencies**: REQ-001, REQ-002, REQ-003

### QR-002

- **Statement**: A dataset result written to `dataset_results.json` is readable from a new store instance after the writing call returns.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` long-term memory; user scope to persist `dataset_results.json`
- **Verification**: Write one record, construct a new store on the same path, and read that record back.
- **Dependencies**: REQ-007

## Availability

None.

## Security

None. Abuse classification is excluded by REQ-005.

## Privacy

None.

## Accessibility

None.

## Observability

None.

## Maintainability

None.

---

## Summary

| Category        | Total | Verified |
| --------------- | ----- | -------- |
| Performance     | 0     | 0        |
| Reliability     | 2     | 2        |
| Availability    | 0     | 0        |
| Security        | 0     | 0        |
| Privacy         | 0     | 0        |
| Accessibility   | 0     | 0        |
| Observability   | 0     | 0        |
| Maintainability | 0     | 0        |
| **Total**       | **2** | **2**    |
