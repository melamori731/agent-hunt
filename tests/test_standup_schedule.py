"""Unit tests for StandupSchedule. REQ-003, REQ-008 timing, DD-004."""

from datetime import datetime, timedelta

from research_orchestrator.schedule import StandupSchedule


def test_standupSchedule_defaultInterval_notDueAt23Hours():
    start = datetime(2026, 11, 20, 0, 0)
    assert StandupSchedule().is_due(start, start + timedelta(hours=23)) is False


def test_standupSchedule_defaultInterval_dueAt24Hours():
    start = datetime(2026, 11, 20, 0, 0)
    assert StandupSchedule().is_due(start, start + timedelta(hours=24)) is True


def test_standupSchedule_oneHour_dueAtOneHour():
    start = datetime(2026, 11, 20, 0, 0)
    assert StandupSchedule(timedelta(hours=1)).is_due(start, start + timedelta(hours=1)) is True


def test_standupSchedule_oneHour_notDueAt59Minutes():
    start = datetime(2026, 11, 20, 0, 0)
    assert StandupSchedule(timedelta(hours=1)).is_due(start, start + timedelta(minutes=59)) is False
