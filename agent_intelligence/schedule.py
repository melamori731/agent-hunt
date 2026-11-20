"""Configured cadence for scheduled discovery."""

from __future__ import annotations

from datetime import datetime, timedelta


class DiscoverySchedule:
    """Decide whether a discovery run is due. The default interval is 24 hours."""

    DEFAULT_INTERVAL = timedelta(hours=24)

    def __init__(self, interval: timedelta | None = None):
        self.interval = self.DEFAULT_INTERVAL if interval is None else interval

    def is_due(self, previous_run: datetime, now: datetime) -> bool:
        return now - previous_run >= self.interval
