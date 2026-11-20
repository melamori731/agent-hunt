(() => {
  const meta = (name) => document.querySelector(`meta[name="${name}"]`)?.content || "";
  const sessionId = meta("sandbox-session-id");
  const telemetryUrl = meta("telemetry-url");
  const page = meta("sandbox-page") || "unknown";
  if (!sessionId || !telemetryUrl) return;

  function webglInfo() {
    try {
      const canvas = document.createElement("canvas");
      const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
      if (!gl) return { vendor: null, renderer: null };
      const dbg = gl.getExtension("WEBGL_debug_renderer_info");
      if (!dbg) return { vendor: gl.getParameter(gl.VENDOR), renderer: gl.getParameter(gl.RENDERER) };
      return {
        vendor: gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL),
        renderer: gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL),
      };
    } catch (_) {
      return { vendor: null, renderer: null };
    }
  }

  function clientHints() {
    const uaData = navigator.userAgentData;
    if (!uaData) {
      return {
        platform: null,
        architecture: null,
        bitness: null,
        mobile: null,
        brands: null,
      };
    }
    return {
      platform: uaData.platform || null,
      architecture: null,
      bitness: null,
      mobile: !!uaData.mobile,
      brands: (uaData.brands || []).map((b) => `${b.brand};v=${b.version}`),
    };
  }

  async function enrichHints(base) {
    const uaData = navigator.userAgentData;
    if (!uaData || !uaData.getHighEntropyValues) return base;
    try {
      const high = await uaData.getHighEntropyValues([
        "architecture",
        "bitness",
        "platform",
        "platformVersion",
        "model",
        "uaFullVersion",
      ]);
      return {
        ...base,
        platform: high.platform || base.platform,
        architecture: high.architecture || null,
        bitness: high.bitness || null,
        platform_version: high.platformVersion || null,
        model: high.model || null,
        ua_full_version: high.uaFullVersion || null,
      };
    } catch (_) {
      return base;
    }
  }

  async function collectFingerprint() {
    const gl = webglInfo();
    const hints = await enrichHints(clientHints());
    return {
      user_agent: navigator.userAgent || null,
      platform: navigator.platform || null,
      language: navigator.language || null,
      languages: Array.from(navigator.languages || []),
      webdriver: !!navigator.webdriver,
      hardware_concurrency: navigator.hardwareConcurrency || null,
      device_memory: navigator.deviceMemory || null,
      max_touch_points: navigator.maxTouchPoints || 0,
      cookie_enabled: !!navigator.cookieEnabled,
      screen: {
        width: screen.width || null,
        height: screen.height || null,
        color_depth: screen.colorDepth || null,
        pixel_ratio: window.devicePixelRatio || null,
      },
      timezone_offset_minutes: new Date().getTimezoneOffset(),
      webgl_vendor: gl.vendor,
      webgl_renderer: gl.renderer,
      client_hints: hints,
      automation_markers: {
        webdriver: !!navigator.webdriver,
        cdc_present: Object.keys(window).some((k) => k.startsWith("cdc_")),
        playwright: !!(window.playwright || window.__playwright),
      },
    };
  }

  async function postEvent(eventType, extra) {
    const fingerprint = await collectFingerprint();
    const payload = {
      session_id: sessionId,
      event_type: eventType,
      page,
      path: location.pathname,
      timestamp: new Date().toISOString(),
      fingerprint,
      ...extra,
    };
    try {
      await fetch(`${telemetryUrl}/v1/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        mode: "cors",
        keepalive: true,
      });
    } catch (_) {
      // Sandbox experiments should tolerate telemetry dropouts; runner can mark blocked.
    }
  }

  postEvent("page_view", {});
  document.addEventListener("submit", () => {
    postEvent("form_submit", {});
  });
})();
