# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

Keep Step 0 coverage in this file. Do not create separate coverage, summary, or overview markdown files for the same requirement mappings.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `suitableDataset_writesEntryForHypothesis` | REQ-001 | A complete candidate becomes one suitable registry entry for the stored hypothesis. |
| `queryOnlyDataset_writesUnsuitable` | REQ-002 | A query-only candidate is stored as unsuitable. |
| `repeatDiscovery_keepsOneEntry` | REQ-003 | A second run for the same dataset and hypothesis leaves one entry. |
| `noSuitableCandidate_writesNoSuitableEntry` | REQ-004 | Failing candidates leave no suitable entry for the hypothesis. |
| `scheduleDue_searchesAgain` | REQ-005 | A suitable entry is searched again when the default interval has elapsed. |
| `scheduleNotDue_skipsSearchWhenSuitableExists` | REQ-005 | A suitable entry is not searched again at 23 hours. |
| `missingSuitable_searchesBeforeInterval` | REQ-005 | A hypothesis with no suitable entry is searched before the interval elapses. |
| `humanText_writesNothing` | REQ-006 | Human text writes no registry entry. |
| `discoveryRun_startsNoShoppingAgentAndWritesNoRule` | REQ-007 | A run starts no shopping agent and writes no hypothesis, metric, or deployed rule. |
| `reopenRegistry_returnsSameEntry` | QR-001 | A new registry instance reads the entry written earlier. |
| `sameCandidate_sameSuitability` | QR-002 | The same candidate and hypothesis receive the same suitability twice. |

---

## Scenarios (Given-When-Then)

### `suitableDataset_writesEntryForHypothesis`

- **Requirements**: REQ-001
- **Given**: One hypothesis file names an id and a list of measurement fields. The catalog returns one dataset with a name, an https source URL, a title, human and agent labels, a session identifier, a license, a verification date inside the age window, and those fields.
- **When**: Discovery runs with no human text.
- **Then**: `datasets.json` has one entry whose dataset name, source URL, title, suitability `suitable`, and hypothesis id match that input.

### `queryOnlyDataset_writesUnsuitable`

- **Requirements**: REQ-002
- **Given**: One stored hypothesis and one catalog candidate flagged as a query-only match.
- **When**: Discovery runs.
- **Then**: The entry for that hypothesis has suitability `unsuitable`.

### `repeatDiscovery_keepsOneEntry`

- **Requirements**: REQ-003
- **Given**: One suitable candidate for one hypothesis.
- **When**: Discovery runs twice.
- **Then**: One entry remains for that dataset name and hypothesis id.

### `noSuitableCandidate_writesNoSuitableEntry`

- **Requirements**: REQ-004
- **Given**: One hypothesis and only candidates that fail a suitability check.
- **When**: Discovery runs.
- **Then**: No entry for that hypothesis has suitability `suitable`.

### `scheduleDue_searchesAgain`

- **Requirements**: REQ-005
- **Given**: A suitable entry exists and the previous scheduled run was 24 hours ago. The interval is the default.
- **When**: Discovery runs.
- **Then**: The catalog is called.

### `scheduleNotDue_skipsSearchWhenSuitableExists`

- **Requirements**: REQ-005
- **Given**: A suitable entry exists and the previous scheduled run was 23 hours ago. The interval is the default.
- **When**: Discovery runs.
- **Then**: The catalog is not called.

### `missingSuitable_searchesBeforeInterval`

- **Requirements**: REQ-005
- **Given**: The previous scheduled run was one minute ago and the hypothesis has no suitable entry.
- **When**: Discovery runs.
- **Then**: The catalog is called and `lastRunAt` stays at that previous time.

### `humanText_writesNothing`

- **Requirements**: REQ-006
- **Given**: A hypothesis file is present and the caller passes human text.
- **When**: Discovery is invoked.
- **Then**: No `datasets.json` entry is written.

### `discoveryRun_startsNoShoppingAgentAndWritesNoRule`

- **Requirements**: REQ-007
- **Given**: One stored hypothesis and one catalog candidate.
- **When**: Discovery runs.
- **Then**: No shopping-agent process starts, the hypothesis file is unchanged, and no validation-metric or deployed-rule record is added.

### `reopenRegistry_returnsSameEntry`

- **Requirements**: QR-001
- **Given**: One registry entry was written to a directory.
- **When**: A new registry opens that directory.
- **Then**: The entry is present.

### `sameCandidate_sameSuitability`

- **Requirements**: QR-002
- **Given**: One candidate and one hypothesis at a fixed time.
- **When**: Suitability is judged twice.
- **Then**: Both judgments return the same suitability.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `suitableDataset_writesEntryForHypothesis` | |
| REQ-002 | `queryOnlyDataset_writesUnsuitable` | |
| REQ-003 | `repeatDiscovery_keepsOneEntry` | |
| REQ-004 | `noSuitableCandidate_writesNoSuitableEntry` | |
| REQ-005 | `scheduleDue_searchesAgain` | Also `scheduleNotDue_skipsSearchWhenSuitableExists` and `missingSuitable_searchesBeforeInterval` |
| REQ-006 | `humanText_writesNothing` | |
| REQ-007 | `discoveryRun_startsNoShoppingAgentAndWritesNoRule` | |
| QR-001 | `reopenRegistry_returnsSameEntry` | |
| QR-002 | `sameCandidate_sameSuitability` | |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 7 | 7 | 0 | 0 |
| QR | 2 | 2 | 0 | 0 |

## Risks and gaps

CA-001 and CA-002 remain planning choices. The scenarios use the 730-day window and the JSON names in DD-004 and DD-005. No live catalog is required.
