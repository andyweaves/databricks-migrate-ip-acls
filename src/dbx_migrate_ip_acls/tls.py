"""Use the operating system's trust store for TLS verification.

In corporate environments a TLS-inspecting proxy presents certificates signed by an internal root CA
that lives in the OS trust store but *not* in certifi's bundle. The Databricks SDK happens to read
the system store, but urllib defaults to certifi — so downloads can fail with
CERTIFICATE_VERIFY_FAILED while the SDK works.

`truststore` makes Python's `ssl` module verify against the OS trust store, fixing every consumer at
once with no env-var fiddling. We call `enable()` once at CLI startup. It's best-effort: if
`truststore` is unavailable or the platform is unsupported, we leave the default (certifi) behaviour
in place, and users can still fall back to SSL_CERT_FILE / REQUESTS_CA_BUNDLE.
"""

from __future__ import annotations

_enabled = False


def enable() -> bool:
    """Inject the OS trust store into Python's ssl module. Idempotent; returns True if active."""
    global _enabled
    if _enabled:
        return True
    try:
        import truststore

        truststore.inject_into_ssl()
        _enabled = True
    except Exception:  # noqa: BLE001 - never let TLS setup crash the CLI
        _enabled = False
    return _enabled
