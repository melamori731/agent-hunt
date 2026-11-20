"""Unit tests for DiscoverySchedule."""

from __future__ import annotations

from datetime import timedelta

from dataset_discovery.schedule import DiscoverySchedule
from tests.helpers import NOW


def test_discoverySchedule_defaultInterval_notDueAt23Hours() -> None:
    schedule = DiscoverySchedule()
    assert schedule.interval == timedelta(hours=24)
    assert schedule.is_due(NOW - timedelta(hours=23), NOW) is False


def test_discoverySchedule_defaultInterval_dueAt24Hours() -> None:
    schedule = DiscoverySchedule()
    assert schedule.is_due(NOW - timedelta(hours=24), NOW) is True


def test_discoverySchedule_oneHour_dueAtOneHour() -> None:
    schedule = DiscoverySchedule(timedelta(hours=1))
    assert schedule.is_due(NOW - timedelta(hours=1), NOW) is True
    assert schedule.is_due(NOW - timedelta(minutes=59), NOW) is False
