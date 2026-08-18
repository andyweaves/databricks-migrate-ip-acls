"""Tag every Databricks SDK request with this tool's name, for usage tracking.

The Databricks SDK appends registered "user-agent extras" to the `User-Agent` header of every API
call it makes. Registering the project name lets platform-side logs attribute API traffic to this
tool. Granularity is **workspace-level** — the cluster/DBU attribution isn't available (cluster ids
are redacted in the logs), so per-DBU attribution isn't possible; the tool name in the User-Agent is
the signal.

Called once at CLI startup, before any WorkspaceClient / AccountClient is constructed (the SDK reads
the registered extras when it builds a client's config).
"""

from __future__ import annotations

from . import __version__

# The identifier platform-side usage queries match on — the project (distribution) name. Appears in
# the User-Agent as `databricks-migrate-ip-acls/<version>`.
PRODUCT_NAME = "databricks-migrate-ip-acls"

_tagged = False


def tag() -> None:
    """Register the tool's name + version as a User-Agent extra. Idempotent per process, and
    best-effort — usage tagging must never break the CLI."""
    global _tagged
    if _tagged:
        return
    try:
        from databricks.sdk.config import with_user_agent_extra

        with_user_agent_extra(PRODUCT_NAME, __version__)
        _tagged = True
    except Exception:  # noqa: BLE001 - never let telemetry setup crash the CLI
        pass
