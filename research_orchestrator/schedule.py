"""Standup timing. The default interval is 24 hours."""

from __future__ import annotations

from datetime import datetime, timedelta


class StandupSchedule:
    DEFAULT_INTERVAL = timedelta(hours=24)

    def __init__(self, interval: timedelta | None = None) -> None:
        self.interval = self.DEFAULT_INTERVAL if interval is None else interval

    def is_due(self, previous: datetime | None, now: datetime) -> bool:
        if previous is None:
            return True
        return now - previous >= self.interval
