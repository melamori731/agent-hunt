# System end-to-end scenarios

One human name moves through stored records. No scenario starts a shopping agent. No scenario deploys a rule.

## Happy path

`humanName_submittedSpec_includesSourcesAndValidation`

A human names Muse. The orchestrator stores one agent-intelligence assignment. Research stores a sourced hypothesis. Dataset discovery stores a suitable dataset. Dataset validation and sandbox validation both support the signal. The rule specification is submitted, not deployed, and contains the research source (url and title) plus both validation results. The evaluator result is PASS. The orchestrator stores that submitted specification with deployed false.

## Failure mode 1

`contradictingValidation_storesNoSubmittedSpec`

Dataset validation supports the signal and the saved sandbox runs contradict it. The system stores no submitted rule specification. The evaluator does not PASS. The orchestrator stores no submitted specification. Nothing is deployed. No shopping agent starts.

## Failure mode 2

`abuseRequest_storesNoAssignment`

The human request asks for abuse classification and does not name research work. The system stores no assignment, no hypothesis, and no rule specification. Nothing is deployed. No shopping agent starts.
