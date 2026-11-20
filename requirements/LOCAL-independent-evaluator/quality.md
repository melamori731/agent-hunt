# Quality Requirements

---

## Performance

None.

## Reliability

### QR-001

- **Statement**: After the process that wrote an evaluation exits, a new reader of evaluations.json returns the same hypothesis_id, stage, result, and trigger.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 7, Traceability
- **Verification**: Write one evaluation, construct a new reader on the same directory, and confirm the stored record matches the written record.
- **Dependencies**: INV-002

### QR-002

- **Statement**: Repeating the same stage check on unchanged stored records appends an evaluation with the same result and the same trigger.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 3, Regression
- **Verification**: Run the same passing hypothesis check twice and confirm the two stored results and triggers are equal.
- **Dependencies**: REQ-001

## Availability

None.

## Security

None.

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
