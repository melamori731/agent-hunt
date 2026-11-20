"""Decide whether a catalog candidate can support one stored hypothesis."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

AGE_WINDOW = timedelta(days=730)


class SuitabilityJudgement:
    """Apply relevance, coverage, and age. A query match alone is unsuitable."""

    def judge(
        self,
        candidate: dict[str, Any],
        hypothesis: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:
        moment = _aware(now)
        suitable = self._checks_pass(candidate, hypothesis, moment)
        return {
            "datasetName": str(candidate.get("datasetName") or ""),
            "sourceUrl": str(candidate.get("sourceUrl") or ""),
            "title": str(candidate.get("title") or ""),
            "suitability": "suitable" if suitable else "unsuitable",
            "hypothesisId": str(hypothesis.get("id") or ""),
            "collectionMethod": str(candidate.get("collectionMethod") or ""),
            "hasSessionIdentifier": candidate.get("hasSessionIdentifier") is True,
            "hasHumanLabel": candidate.get("hasHumanLabel") is True,
            "hasAgentLabel": candidate.get("hasAgentLabel") is True,
            "license": str(candidate.get("license") or ""),
            "verifiedAt": str(candidate.get("verifiedAt") or ""),
        }

    def _checks_pass(
        self,
        candidate: dict[str, Any],
        hypothesis: dict[str, Any],
        now: datetime,
    ) -> bool:
        if candidate.get("queryMatchOnly") is True:
            return False
        if not str(candidate.get("datasetName") or "").strip():
            return False
        if not str(candidate.get("title") or "").strip():
            return False
        if not _http_url(str(candidate.get("sourceUrl") or "")):
            return False
        if candidate.get("hasHumanLabel") is not True:
            return False
        if candidate.get("hasAgentLabel") is not True:
            return False
        if candidate.get("hasSessionIdentifier") is not True:
            return False
        if not str(candidate.get("license") or "").strip():
            return False
        verified = _parse_time(candidate.get("verifiedAt"))
        if verified is None or verified > now or verified < now - AGE_WINDOW:
            return False
        required = hypothesis.get("measurementFields") or []
        if not required:
            return False
        fields = candidate.get("fields")
        if not isinstance(fields, list):
            return False
        return all(field in fields for field in required)


def _http_url(value: str) -> bool:
    return value.startswith(("https://", "http://"))


def _aware(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def _parse_time(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return _aware(parsed)
