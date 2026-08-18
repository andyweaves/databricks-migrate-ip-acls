"""Databricks authentication via the SDK's unified auth.

Workspace calls resolve credentials from the usual chain (a `--profile` in ~/.databrickscfg,
`DATABRICKS_*` env vars, or OAuth). Account-level calls (creating/assigning a policy, the migration
pre-checks) need an **account admin**; the recommended path is an account-admin service principal via
OAuth M2M, configured in the same profile/env. We don't invent a bespoke secret path: whatever the
SDK's unified auth resolves for the account is used.
"""

from __future__ import annotations

from functools import cache

from databricks.sdk import AccountClient, WorkspaceClient

from .config import Connection


@cache
def _workspace_client(profile: str | None) -> WorkspaceClient:
    return WorkspaceClient(profile=profile) if profile else WorkspaceClient()


def workspace_client(conn: Connection) -> WorkspaceClient:
    """A WorkspaceClient for reading the workspace's IP access lists + enforcement toggle."""
    return _workspace_client(conn.profile)


def account_client(conn: Connection) -> AccountClient:
    """An account-admin AccountClient for the migration pre-checks + applying the policy.

    Requires an account_id (not reliably discoverable from a workspace runtime) and account-admin
    credentials resolved by unified auth for the account host. Raises a clear, actionable error when
    the account_id is missing."""
    if not conn.account_id:
        raise ValueError(
            "This operation is account-level and needs a Databricks account_id, which is not set.\n"
            "  Pass --account-id <numeric id> (find it in the Account console top-right user menu,\n"
            "  or in the account console URL after '/account/'). Account-admin credentials must be\n"
            "  resolvable for the account host."
        )
    # A dedicated --account-profile wins; otherwise let unified auth resolve account creds from env
    # or a matching profile. We deliberately do NOT forward the workspace --profile here: a
    # workspace OAuth session can't authenticate to the account API ("Unable to load OAuth Config").
    if conn.account_profile:
        return AccountClient(profile=conn.account_profile)
    return AccountClient(host=conn.account_host, account_id=conn.account_id)


def this_workspace_id(conn: Connection) -> int:
    return workspace_client(conn).get_workspace_id()
