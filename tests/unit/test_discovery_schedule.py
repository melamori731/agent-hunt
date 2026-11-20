"""Unit tests for DiscoverySchedule."""

from datetime import timedelta

from agent_intelligence import DiscoverySchedule
from tests.support import T0, hours_after


def discoverySchedule_defaultInterval_notDueAt23Hours():
    """The default 24-hour interval is not due at 23 hours."""
    schedule = DiscoverySchedule()
    assert schedule.interval == timedelta(hours=24)
    assert schedule.is_due(T0, hours_after(23)) is False


def discoverySchedule_defaultInterval_dueAt24Hours():
    """The default interval is due at 24 hours."""
    schedule = DiscoverySchedule()
    assert schedule.is_due(T0, hours_after(24)) is True


def discoverySchedule_oneHour_dueAtOneHour():
    """A 1-hour interval is due at 1 hour."""
    schedule = DiscoverySchedule(timedelta(hours=1))
    assert schedule.is_due(T0, hours_after(1)) is True
