#!/usr/bin/env python3
"""Execute sandbox scenarios and evaluate signal reproducibility.

Example:
  python run_scenario.py --scenario scenarios/muse_fingerprint.yaml --runs 5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import yaml

from evaluate import signal_present, summarize_runs
from profiles import get_profile

STORE_URL = os.environ.get("STORE_URL", "http://localhost:8080").rstrip("/")
TELEMETRY_URL = os.environ.get("TELEMETRY_URL", "http://localhost:8090").rstrip("/")
RESULTS_DIR = Path(os.environ.get("RESULTS_DIR", "results"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_scenario(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "id" not in data:
        raise ValueError(f"Invalid scenario file: {path}")
    return data


def wait_for_services(timeout_s: float = 60.0) -> None:
    deadline = time.time() + timeout_s
    last_error = ""
    while time.time() < deadline:
        try:
            with httpx.Client(timeout=3.0) as client:
                store = client.get(f"{STORE_URL}/health")
                tele = client.get(f"{TELEMETRY_URL}/health")
                if store.status_code == 200 and tele.status_code == 200:
                    return
                last_error = f"store={store.status_code} telemetry={tele.status_code}"
        except Exception as exc:  # noqa: BLE001 - surface readiness errors
            last_error = str(exc)
        time.sleep(1.0)
    raise RuntimeError(f"Services not ready after {timeout_s}s: {last_error}")


def browse_store(client: httpx.Client, session_id: str) -> None:
    """Walk a simple browse → cart → checkout path against the mock store."""
    headers = {"Cookie": f"sandbox_session_id={session_id}"}
    home = client.get(f"{STORE_URL}/", headers=headers)
    home.raise_for_status()
    products = client.get(f"{STORE_URL}/api/products", headers=headers)
    products.raise_for_status()
    product_id = products.json()[0]["id"]
    add = client.post(
        f"{STORE_URL}/api/cart/add",
        headers={**headers, "Content-Type": "application/json"},
        json={"product_id": product_id, "quantity": 1},
    )
    add.raise_for_status()
    cart = client.get(f"{STORE_URL}/cart", headers=headers)
    cart.raise_for_status()
    checkout = client.get(f"{STORE_URL}/checkout", headers=headers)
    checkout.raise_for_status()
    receipt = client.post(
        f"{STORE_URL}/checkout",
        headers=headers,
        data={"name": "Sandbox Runner", "email": "runner@example.com"},
    )
    receipt.raise_for_status()


def inject_telemetry(
    client: httpx.Client,
    *,
    session_id: str,
    run_id: str,
    scenario: dict[str, Any],
    profile_name: str,
    profile: dict[str, Any],
) -> None:
    payload = {
        "session_id": session_id,
        "event_type": "synthetic_session",
        "page": "runner",
        "path": "/synthetic",
        "timestamp": _now(),
        "fingerprint": profile["fingerprint"],
        "profile": profile_name,
        "scenario_id": scenario["id"],
        "run_id": run_id,
        "labels": {
            "population": profile.get("label"),
            "agent_family": profile.get("agent_family"),
        },
    }
    resp = client.post(f"{TELEMETRY_URL}/v1/events", json=payload)
    resp.raise_for_status()


def execute_run(
    client: httpx.Client,
    *,
    scenario: dict[str, Any],
    profile_name: str,
    attempt: int,
) -> dict[str, Any]:
    run_id = f"{scenario['id']}-{attempt}-{uuid.uuid4().hex[:8]}"
    session_id = str(uuid.uuid4())
    profile = get_profile(profile_name)
    result: dict[str, Any] = {
        "attempt": attempt,
        "run_id": run_id,
        "session_id": session_id,
        "profile": profile_name,
        "started_at": _now(),
    }
    try:
        browse_store(client, session_id)
        inject_telemetry(
            client,
            session_id=session_id,
            run_id=run_id,
            scenario=scenario,
            profile_name=profile_name,
            profile=profile,
        )
        session = client.get(f"{TELEMETRY_URL}/v1/sessions/{session_id}")
        session.raise_for_status()
        body = session.json()
        fingerprint = body.get("latest_fingerprint") or {}
        if not fingerprint:
            result.update(
                {
                    "status": "blocked",
                    "reason": "telemetry_missing_fingerprint",
                    "signal_observed": False,
                }
            )
            return result
        observed = signal_present(fingerprint, scenario["signal"])
        result.update(
            {
                "status": "ok",
                "signal_observed": observed,
                "fingerprint": fingerprint,
                "event_count": len(body.get("events", [])),
            }
        )
        return result
    except Exception as exc:  # noqa: BLE001 - capture per-run failures
        result.update(
            {
                "status": "blocked",
                "reason": str(exc),
                "signal_observed": False,
            }
        )
        return result
    finally:
        result["finished_at"] = _now()


def run_scenario(
    scenario_path: Path,
    *,
    runs: int | None = None,
    profile_override: str | None = None,
) -> dict[str, Any]:
    scenario = load_scenario(scenario_path)
    profile_name = profile_override or scenario.get("profile", "muse_like")
    threshold = scenario.get("reproducibility", {})
    threshold_positives = int(threshold.get("positives", 4))
    threshold_window = int(threshold.get("window", 5))
    max_attempts = int(threshold.get("max_attempts", 10))
    attempt_count = runs if runs is not None else threshold_window

    wait_for_services()
    run_records: list[dict[str, Any]] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        for attempt in range(1, attempt_count + 1):
            run_records.append(
                execute_run(
                    client,
                    scenario=scenario,
                    profile_name=profile_name,
                    attempt=attempt,
                )
            )

    summary = summarize_runs(
        run_records,
        threshold_positives=threshold_positives,
        threshold_window=threshold_window,
        max_attempts=max_attempts,
    )
    report = {
        "scenario_id": scenario["id"],
        "scenario_path": str(scenario_path),
        "hypothesis_id": scenario.get("hypothesis_id"),
        "description": scenario.get("description"),
        "profile": profile_name,
        "generated_at": _now(),
        "summary": summary,
        "runs": run_records,
        "limitations": scenario.get(
            "limitations",
            [
                "Synthetic fingerprints do not establish human false-positive rates.",
                "Sandbox reproduction alone is insufficient for production rules.",
            ],
        ),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / f"{scenario['id']}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["report_path"] = str(out)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an agent-hunt sandbox scenario")
    parser.add_argument(
        "--scenario",
        default=None,
        help="Path to scenario YAML",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=None,
        help="Number of independent runs (default: scenario window)",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Override profile name (human_desktop, muse_like, generic_bot)",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="Print available profiles and exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list_profiles:
        from profiles import PROFILES

        for name, meta in PROFILES.items():
            print(f"{name}\tlabel={meta.get('label')}\tfamily={meta.get('agent_family', '-')}")
        return 0

    if not args.scenario:
        parser.error("--scenario is required unless --list-profiles is set")

    report = run_scenario(
        Path(args.scenario),
        runs=args.runs,
        profile_override=args.profile,
    )
    summary = report["summary"]
    print(json.dumps({"scenario_id": report["scenario_id"], "summary": summary, "report_path": report["report_path"]}, indent=2))
    if summary["conclusion"] == "blocked":
        return 2
    if summary["conclusion"] == "not_reproduced":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
