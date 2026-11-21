"""Telemetry collector for sandbox browser and session fingerprints."""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data/sessions"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

_LOCK = threading.Lock()
_EVENTS: list[dict[str, Any]] = []
_SESSIONS: dict[str, dict[str, Any]] = {}

app = FastAPI(title="Agent Hunt Sandbox Telemetry", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TelemetryEvent(BaseModel):
    session_id: str
    event_type: str
    page: str | None = None
    path: str | None = None
    timestamp: str | None = None
    fingerprint: dict[str, Any] = Field(default_factory=dict)
    profile: str | None = None
    scenario_id: str | None = None
    run_id: str | None = None
    labels: dict[str, Any] = Field(default_factory=dict)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _persist_session(session_id: str) -> None:
    session = _SESSIONS.get(session_id)
    if not session:
        return
    path = DATA_DIR / f"{session_id}.json"
    path.write_text(json.dumps(session, indent=2, sort_keys=True), encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "telemetry"}


@app.post("/v1/events")
def ingest_event(event: TelemetryEvent) -> dict[str, Any]:
    record = event.model_dump()
    record["received_at"] = _now()
    record["event_id"] = str(uuid.uuid4())
    if not record.get("timestamp"):
        record["timestamp"] = record["received_at"]

    with _LOCK:
        _EVENTS.append(record)
        session = _SESSIONS.setdefault(
            event.session_id,
            {
                "session_id": event.session_id,
                "created_at": record["received_at"],
                "updated_at": record["received_at"],
                "profile": event.profile,
                "scenario_id": event.scenario_id,
                "run_id": event.run_id,
                "labels": event.labels,
                "events": [],
                "latest_fingerprint": {},
            },
        )
        session["updated_at"] = record["received_at"]
        session["events"].append(record)
        if event.fingerprint:
            session["latest_fingerprint"] = event.fingerprint
        if event.profile:
            session["profile"] = event.profile
        if event.scenario_id:
            session["scenario_id"] = event.scenario_id
        if event.run_id:
            session["run_id"] = event.run_id
        if event.labels:
            session["labels"] = {**session.get("labels", {}), **event.labels}
        _persist_session(event.session_id)

    return {"ok": True, "event_id": record["event_id"]}


@app.get("/v1/sessions")
def list_sessions() -> list[dict[str, Any]]:
    with _LOCK:
        return [
            {
                "session_id": s["session_id"],
                "created_at": s["created_at"],
                "updated_at": s["updated_at"],
                "profile": s.get("profile"),
                "scenario_id": s.get("scenario_id"),
                "run_id": s.get("run_id"),
                "event_count": len(s.get("events", [])),
            }
            for s in _SESSIONS.values()
        ]


@app.get("/v1/sessions/{session_id}")
def get_session(session_id: str) -> dict[str, Any]:
    with _LOCK:
        session = _SESSIONS.get(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="session_not_found")
        return session


@app.delete("/v1/sessions")
def clear_sessions() -> dict[str, Any]:
    with _LOCK:
        count = len(_SESSIONS)
        _SESSIONS.clear()
        _EVENTS.clear()
        for path in DATA_DIR.glob("*.json"):
            path.unlink(missing_ok=True)
    return {"ok": True, "cleared": count}
