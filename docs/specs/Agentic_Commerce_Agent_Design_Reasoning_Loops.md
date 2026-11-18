# Autonomous Threat Detection Researcher for Agentic Commerce

Initial scope: Identify AI shopping sessions and distinguish them from human shopping sessions. Classification of legitimate versus abusive AI agents is deferred to a later phase.

Four specialist agents execute separate reasoning loops. An orchestrator assigns work and tracks progress. Agents do not reason together or exchange messages directly; outputs are stored as structured records.

## 1. Reasoning loops

### Threat Intelligence & Hypothesis Generation Agent

1. Search current technical publications, agent documentation, and product announcements for implementations of AI shopping agents.
2. Extract implementation details that could be visible in session telemetry: User-Agent values, IP ranges, browser automation behaviour, or device fingerprints.
3. Formulate a testable hypothesis identifying the proposed signal, expected observation, supporting sources, and required measurements.
4. Check stored hypotheses and past investigations for duplicates, contradictory findings, or unresolved questions.
5. Retrieve additional evidence and refine the hypothesis if the signal or test conditions are insufficiently specified.
6. Store the hypothesis and source references when testable; otherwise record the unresolved issue and stop.

**Example:** Documentation describing a browser running in a virtual machine suggests testing virtualisation-related fingerprint attributes. This is a hypothesis, not proof that virtualisation identifies AI sessions.

### Dataset Validation Agent

1. Translate the hypothesis into dataset requirements: labels for human and AI sessions, required telemetry fields, sample coverage, and data-quality criteria.
2. Search accessible labelled datasets and inspect their schemas and metadata.
3. Stop and report unmet criteria if no dataset qualifies; do not substitute data missing the required measurements.
4. Select comparisons and metrics, including signal prevalence across classes and false-positive rate.
5. Run Python analysis, inspect the results for confounding factors, and repeat calculations if warranted.
6. Store a report with the dataset, method, metrics, conclusion, and limitations; mark insufficient evidence as inconclusive.

### Sandbox Validation Agent

1. Define the expected signal and select a scenario in the preconfigured, instrumented e-commerce sandbox.
2. Specify controlled conditions, telemetry to collect, a reproducibility threshold, and a maximum number of attempts.
3. Execute the scenario with an AI shopping agent and capture browser and session telemetry.
4. Compare observed signals with the hypothesis; repeat independent runs under equivalent conditions.
5. Stop when the reproducibility threshold is met or the attempt limit is reached. Report blocked experiments if required telemetry cannot be collected.
6. Store the experimental setup, run-level evidence, reproduction rate, conclusion, and limitations.

**Provisional stopping rule:** At least four positive observations in five independent runs; no more than ten attempts. Sandbox reproduction alone does not establish a low false-positive rate for human sessions.

### Detection Rule Specification Agent

1. Retrieve the hypothesis and all available dataset and sandbox validation reports.
2. Check whether at least one validation supports the signal; flag contradictory findings for further investigation.
3. Define required telemetry fields, detection conditions, thresholds, and known exceptions.
4. Assign an evidence-confidence level based on the available validation methods and their limitations.
5. Check that each condition is supported by the recorded evidence; revise or reject unsupported conditions.
6. Store a versioned, machine-readable rule specification for human review; do not deploy it.

### Orchestrator

1. At scheduled research standups, retrieve new hypotheses, active investigations, blocked tasks, and completed reports.
2. Identify hypotheses awaiting validation and assign them to the dataset and sandbox validators.
3. Review completed results: one positive result may justify rule specification when the other test is blocked or inconclusive, with lower confidence.
4. Route conflicting results or insufficiently defined hypotheses back for further investigation.
5. Request rule specifications for eligible hypotheses; record decisions, task status, and next actions before ending the standup.

## 2. Memory

**Short-term memory:** Each agent retains sources, intermediate observations, calculations, experiment counters, draft rule conditions, or standup decisions during its current run. These records determine the next action and whether stopping criteria have been met.

**Long-term memory:** Persistent storage retains hypotheses, validation reports, rule specifications, and overall research status, including blocked items and hypotheses requiring refinement. Versioned records link each rule to its source hypothesis and experimental evidence.

## 3. External tools

Web search and document retrieval provide current technical information for hypothesis retrieval and grounding. Dataset access retrieves labelled human and AI session records. Python computes signal prevalence, false-positive rates, and other validation metrics. Sandbox execution and telemetry collection ground hypotheses in observed behaviour; repeated runs measure reproducibility. Persistent storage preserves research state across runs.

Tool use is necessary to test whether a proposed fingerprint signal appears in actual session records. A prompt-only model cannot measure its prevalence or false-positive rate without access to those records and computation.

## 4. Improvement over prompt-only reasoning

Source references are required for hypotheses; dataset measurements or reproducible sandbox observations are required before a detection rule can be specified. Missing data, conflicting results, and unsuccessful reproduction are recorded rather than replaced with model assumptions. Rules supported by only one validation method receive lower evidence confidence.

**Failure mode:** An LLM may propose detection rules based on unverified assumptions, leading to false positives.
