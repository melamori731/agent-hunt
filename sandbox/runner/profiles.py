"""Synthetic browser profiles for controlled sandbox experiments.

These profiles inject fingerprint fields the telemetry collector would otherwise
observe from a real browser. They let the Sandbox Validation Agent reproduce
signal hypotheses without requiring a headed browser inside Docker.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

PROFILES: dict[str, dict[str, Any]] = {
    "human_desktop": {
        "label": "human",
        "fingerprint": {
            "user_agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
            ),
            "platform": "MacIntel",
            "language": "en-US",
            "languages": ["en-US", "en"],
            "webdriver": False,
            "hardware_concurrency": 8,
            "device_memory": 8,
            "max_touch_points": 0,
            "cookie_enabled": True,
            "screen": {"width": 1440, "height": 900, "color_depth": 30, "pixel_ratio": 2},
            "timezone_offset_minutes": 0,
            "webgl_vendor": "Apple Inc.",
            "webgl_renderer": "Apple M2",
            "client_hints": {
                "platform": "macOS",
                "architecture": "arm",
                "bitness": "64",
                "mobile": False,
                "brands": ["Not/A)Brand;v=8", "Chromium;v=0"],
            },
            "automation_markers": {
                "webdriver": False,
                "cdc_present": False,
                "playwright": False,
            },
        },
    },
    "muse_like": {
        "label": "ai_agent",
        "agent_family": "muse_like",
        "fingerprint": {
            # Matches the H1 example from the retrieval checkpoint docs:
            # Linux/Chromium UA, architecture hint mismatch, software WebGL, webdriver=false.
            "user_agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
            ),
            "platform": "Linux x86_64",
            "language": "en-US",
            "languages": ["en-US"],
            "webdriver": False,
            "hardware_concurrency": 6,
            "device_memory": 8,
            "max_touch_points": 0,
            "cookie_enabled": True,
            "screen": {"width": 1920, "height": 1080, "color_depth": 24, "pixel_ratio": 1},
            "timezone_offset_minutes": 0,
            "webgl_vendor": "Google Inc. (Google)",
            "webgl_renderer": "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device), SwiftShader)",
            "client_hints": {
                "platform": "Linux",
                "architecture": "arm",
                "bitness": "64",
                "mobile": False,
                "brands": ["Chromium;v=154", "Not-A.Brand;v=99", "Google Chrome;v=154"],
            },
            "automation_markers": {
                "webdriver": False,
                "cdc_present": False,
                "playwright": False,
            },
        },
    },
    "generic_bot": {
        "label": "ai_agent",
        "agent_family": "generic_bot",
        "fingerprint": {
            "user_agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) HeadlessChrome/120.0.0.0 Safari/537.36"
            ),
            "platform": "Linux x86_64",
            "language": "en-US",
            "languages": ["en-US"],
            "webdriver": True,
            "hardware_concurrency": 2,
            "device_memory": 2,
            "max_touch_points": 0,
            "cookie_enabled": True,
            "screen": {"width": 800, "height": 600, "color_depth": 24, "pixel_ratio": 1},
            "timezone_offset_minutes": 0,
            "webgl_vendor": "Google Inc. (Google)",
            "webgl_renderer": "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device), SwiftShader)",
            "client_hints": {
                "platform": "Linux",
                "architecture": "x86",
                "bitness": "64",
                "mobile": False,
                "brands": ["HeadlessChrome;v=120", "Chromium;v=120"],
            },
            "automation_markers": {
                "webdriver": True,
                "cdc_present": True,
                "playwright": False,
            },
        },
    },
}


def get_profile(name: str) -> dict[str, Any]:
    if name not in PROFILES:
        known = ", ".join(sorted(PROFILES))
        raise KeyError(f"Unknown profile '{name}'. Known: {known}")
    return deepcopy(PROFILES[name])
