"""Decide when a scheduled dataset search is due."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


class DiscoverySchedule:
    """Default interval is 24 hours. A missing previous run is due."""

    def __init__(self, interval: timedelta | None = None) -> None:
        self.interval = timedelta(hours=24) if interval is None else interval

    def is_due(self, last_run_at: datetime | None, now: datetime) -> bool:
        if last_run_at is None:
            return True
        return _aware(now) - _aware(last_run_at) >= self.interval


def _aware(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)
