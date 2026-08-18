"""Tests for the User-Agent usage tag."""

from __future__ import annotations

from dbx_migrate_ip_acls import __version__, usage


def test_tag_adds_product_to_user_agent():
    usage.tag()
    from databricks.sdk.useragent import to_string
    assert f"databricks-migrate-ip-acls/{__version__}" in to_string()


def test_tag_is_idempotent():
    # called at startup (and possibly again); the token must appear exactly once, never duplicated.
    usage.tag()
    usage.tag()
    from databricks.sdk.useragent import to_string
    assert to_string().count("databricks-migrate-ip-acls/") == 1
