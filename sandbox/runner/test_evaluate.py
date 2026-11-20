from evaluate import match_condition, signal_present, summarize_runs


def test_match_condition_ops():
    fp = {
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/154.0.0.0",
        "webdriver": False,
        "client_hints": {"architecture": "arm"},
        "webgl_renderer": "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device), SwiftShader)",
    }
    assert match_condition(fp, {"field": "webdriver", "op": "eq", "value": False})
    assert match_condition(fp, {"field": "user_agent", "op": "contains", "value": "Linux x86_64"})
    assert match_condition(fp, {"field": "webgl_renderer", "op": "regex", "value": "(?i)swiftshader"})
    assert match_condition(fp, {"field": "client_hints.architecture", "op": "eq", "value": "arm"})
    assert match_condition(fp, {"field": "missing", "op": "exists"}) is False


def test_signal_present_all_and_any():
    fp = {"webdriver": True, "platform": "Linux"}
    assert signal_present(
        fp,
        {
            "mode": "all",
            "conditions": [
                {"field": "webdriver", "op": "eq", "value": True},
                {"field": "platform", "op": "eq", "value": "Linux"},
            ],
        },
    )
    assert not signal_present(
        fp,
        {
            "mode": "all",
            "conditions": [
                {"field": "webdriver", "op": "eq", "value": True},
                {"field": "platform", "op": "eq", "value": "Windows"},
            ],
        },
    )
    assert signal_present(
        fp,
        {
            "mode": "any",
            "conditions": [
                {"field": "platform", "op": "eq", "value": "Windows"},
                {"field": "webdriver", "op": "eq", "value": True},
            ],
        },
    )


def test_summarize_runs_reproduced():
    runs = [{"status": "ok", "signal_observed": True} for _ in range(5)]
    summary = summarize_runs(runs, threshold_positives=4, threshold_window=5, max_attempts=10)
    assert summary["conclusion"] == "reproduced"
    assert summary["met_threshold"] is True


def test_summarize_runs_blocked():
    runs = [{"status": "blocked", "signal_observed": False} for _ in range(3)]
    summary = summarize_runs(runs, threshold_positives=4, threshold_window=5, max_attempts=10)
    assert summary["conclusion"] == "blocked"


def test_summarize_runs_not_reproduced_after_full_window():
    runs = [{"status": "ok", "signal_observed": False} for _ in range(5)]
    summary = summarize_runs(runs, threshold_positives=4, threshold_window=5, max_attempts=10)
    assert summary["conclusion"] == "not_reproduced"
    assert summary["met_threshold"] is False
