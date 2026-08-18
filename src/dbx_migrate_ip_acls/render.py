"""Presentation layer: turn engine results into Rich output.

Kept separate from the engine (pure logic) and cli.py (arg parsing / flow) so each function takes an
analysis/result object and prints.
"""

from __future__ import annotations

import pandas as pd

from . import console
from .config import AclConfig


# ------------------------------------------------------------------------------------- decisions
def acl_decisions(cfg: AclConfig) -> None:
    console.decisions_panel("IP ACL → CBI migration configuration", [
        ("policy_mode", cfg.policy_mode, "enforce (default) or dry_run."),
        ("policy_name", cfg.policy_name, "Policy id for the new policy (from --policy-name / prompt)."),
        ("auto_assign", cfg.auto_assign, "Bind this workspace to the new policy."),
        ("disable_existing_ip_acls", cfg.disable_existing_ip_acls,
         "After apply, turn off the workspace's IP access lists (needs create + assign)."),
        ("export", cfg.export,
         "Path to write the proposed policy as JSON + Terraform (.tf); '.' = current directory."),
        ("create_policy", cfg.create_policy, "Master switch: nothing is written unless true."),
    ])


# ---------------------------------------------------------------------------------- acl tables
def _acl_table(rows: list[dict], title: str) -> None:
    console.dataframe(
        pd.DataFrame([{**a, "ip_addresses": ", ".join(a["ip_addresses"])} for a in rows]), title)


def acl_current_config(analysis) -> None:
    """The workspace's *current* IP access list configuration — all lists, enabled and disabled —
    shown when the workspace toggle is off so the user sees what they'd be enabling."""
    console.rule("Current IP access list configuration")
    rows = ([{**a, "enabled": True} for a in analysis.ip_acls]
            + [{**a, "enabled": False} for a in analysis.disabled_acls])
    if rows:
        _acl_table(rows, f"IP access lists on workspace {analysis.workspace_id}")


def acl_analysis(analysis, cfg: AclConfig) -> None:
    console.rule("Existing IP access list")
    if not analysis.ip_acls:
        console.banner("warn", "No enabled IP access lists on this workspace — nothing to migrate.")
        return
    _acl_table(analysis.ip_acls, f"Enabled IP access lists on workspace {analysis.workspace_id}")


def acl_disabled_notice(analysis) -> None:
    """Shown in the final printout (below the old + new policy, before the write): flag any disabled
    IP access list rules that were left out of the migration so the operator can vet them."""
    if not analysis.disabled_acls:
        return
    names = ", ".join(a["label"] for a in analysis.disabled_acls)
    console.banner("warn", f"{len(analysis.disabled_acls)} rule(s) are disabled in IP access lists "
                           f"and were NOT migrated: {names}. Make sure you vet these rules — if any "
                           "should be enabled, exit this tool, enable them, and run the migration "
                           "again.")


def acl_preview(preview: dict, cfg: AclConfig) -> None:
    console.rule("Proposed policy — JSON preview")
    console.banner("warn", "Please review the proposed context-based ingress policy carefully "
                           "before applying.")
    console.json_panel(f"`{cfg.policy_mode_target}` block", preview)


# ------------------------------------------------------------------------------- apply results
def policy_url(account_host: str, account_id: str, policy_id: str) -> str:
    """The account-console URL for a network policy."""
    host = (account_host or "").rstrip("/")
    return f"{host}/security/networking/network-access-policies/{policy_id}?account_id={account_id}"


def apply_results(results: list[dict], account_host: str = "", account_id: str = "") -> None:
    console.rule("Apply results")
    for r in results:
        if "error" in r:
            console.banner("danger", f"target {r['target']}: {r['error']}")
            continue
        msg = f"{r['action']} network policy"
        if r.get("assigned") is not None:
            msg += f" and bound workspace {r['assigned']}"
        console.banner("success", msg)
        console.console.print(f"   [key]network policy id:[/key] {r['policy_id']}")
        if account_host and account_id:
            url = policy_url(account_host, account_id, r["policy_id"])
            # soft_wrap keeps the URL on one logical line (terminals still soft-wrap the display,
            # but it stays a single copy-pasteable string and isn't hard-broken mid-token).
            console.console.print(f"   [key]url:[/key] [info]{url}[/info]", soft_wrap=True)
