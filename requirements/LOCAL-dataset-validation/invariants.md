# Invariants

Stable truths the system must never violate.

---

## Data invariants

### INV-001

- **Statement**: Every stored `result` is one of support, contradict, inconclusive, or blocked.
- **Source**: User scope for the result field
- **Verification**: Attempt to store a result outside those four values and confirm it is rejected.
- **If violated**: Coordinating agents cannot tell what the measurement decided.

### INV-002

- **Statement**: Support is stored only when `prevalence` and `false_positive_rate` are numbers and `prevalence` is strictly greater; contradict is stored only when both are numbers and `prevalence` is strictly less; inconclusive is stored when the two numbers are equal or both are null; blocked is stored only when both are null.
- **Source**: User definitions of the four results; ASS-002
- **Verification**: Reject a support record whose prevalence is not strictly greater than its false-positive rate, and reject a blocked record that carries a number.
- **If violated**: The result word disagrees with the stored rates.

## Integrity invariants

None.

## Business logic invariants

None.

## Security invariants

None.

## Consistency invariants

None.

---

## Summary

- **Total invariants**: 2
