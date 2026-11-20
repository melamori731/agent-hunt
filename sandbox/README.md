# Agent Hunt Sandbox

Local Docker sandbox for the **Sandbox Validation** agent described in the design specs.

It provides:

1. An instrumented mock e-commerce store
2. A telemetry collector for session / browser fingerprints
3. Synthetic agent and human profiles
4. Scenario runners that measure signal reproducibility (default rule: ≥4 positives in 5 runs)

This is intentionally lighter than WebArena: enough controlled surface to validate fingerprint hypotheses without a full browser farm.

## Quick start

```bash
cd sandbox
docker compose up -d --build store telemetry
make smoke
```

Store: http://localhost:8080  
Telemetry: http://localhost:8090

Run the Muse-like fingerprint scenario:

```bash
make scenario SCENARIO=scenarios/muse_fingerprint.yaml RUNS=5
```

Or directly:

```bash
docker compose run --rm runner \
  --scenario /app/scenarios/muse_fingerprint.yaml \
  --runs 5
```

Reports land in `data/results/`. Session JSON lands in `data/sessions/`.

## Profiles

| Profile | Population | Notes |
|---|---|---|
| `human_desktop` | human | macOS Safari-like fingerprint |
| `muse_like` | ai_agent | Linux/Chromium + ARM hint + SwiftShader, `webdriver=false` |
| `generic_bot` | ai_agent | HeadlessChrome with `webdriver=true` |

List profiles:

```bash
make profiles
```

Negative control (human profile against Muse signal — expect `not_reproduced`, 0 positives):

```bash
make scenario SCENARIO=scenarios/muse_fingerprint.yaml PROFILE=human_desktop RUNS=5
```

The runner reaches store/telemetry through `host.docker.internal` (published host ports). That keeps scenario runs working even when Docker bridge container-to-container routing is restricted.

## Scenario format

YAML under `scenarios/`:

```yaml
id: muse_fingerprint
hypothesis_id: H1
profile: muse_like
signal:
  mode: all   # or any
  conditions:
    - field: webgl_renderer
      op: regex
      value: "(?i)swiftshader|angle"
reproducibility:
  positives: 4
  window: 5
  max_attempts: 10
```

Supported condition ops: `eq`, `ne`, `contains`, `regex`, `exists`, `in`, `gte`, `lte`.

## API surface

### Store

- `GET /` catalog
- `GET /api/products`
- `POST /api/cart/add`
- `GET /cart`, `GET /checkout`
- Browser pages load `/static/telemetry.js` and emit fingerprints when opened in a real browser

### Telemetry

- `POST /v1/events` ingest fingerprint event
- `GET /v1/sessions` list sessions
- `GET /v1/sessions/{id}` full session + events
- `DELETE /v1/sessions` clear persisted sessions

## Unit tests

```bash
make test-unit
```

## Design mapping

| Spec concept | Sandbox piece |
|---|---|
| Preconfigured e-commerce sandbox | `store` service |
| Telemetry collection | `telemetry` + `telemetry.js` |
| Controlled AI shopping agent run | `runner` + profiles |
| Reproducibility threshold (4/5, max 10) | scenario YAML + `evaluate.summarize_runs` |
| Hypothesis H1 Muse fingerprint | `scenarios/muse_fingerprint.yaml` |

## Limits

- Synthetic profiles do **not** prove human false-positive rates.
- Real headed-browser capture is optional future work; the current runner injects profile fingerprints after driving the shop HTTP path.
- Not a substitute for labelled dataset validation.
