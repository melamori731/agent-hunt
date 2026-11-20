# agent-hunt

Autonomous threat-detection research agent for **agentic commerce**: discover and experimentally validate behavioural signals that separate human shoppers, legitimate AI shopping agents, and abusive agents.

## Repository layout

| Path | Contents |
|---|---|
| `docs/specs/` | Capstone design documents (architecture, safety, multi-agent coordination) |
| `sandbox/` | Local Docker sandbox for Sandbox Validation experiments |

## Local sandbox

Spin up an instrumented mock shop + telemetry collector, then run reproducibility scenarios:

```bash
cd sandbox
docker compose up -d --build store telemetry
make smoke
make scenario SCENARIO=scenarios/muse_fingerprint.yaml RUNS=5
```

See [`sandbox/README.md`](sandbox/README.md) for profiles, scenario YAML, and APIs.
