"""Tests for the best-effort Terraform (HCL) rendering of a proposed network policy."""

from __future__ import annotations

from dbx_migrate_ip_acls import terraform

_POLICY = {
    "network_policy_id": "my-acl",
    "account_id": "acc-123",
    "ingress": {
        "public_access": {
            "restriction_mode": "RESTRICTED_ACCESS",
            "allow_rules": [
                {"label": "office",
                 "origin": {"included_ip_ranges": {"ip_ranges": ["8.8.8.8/32", "9.9.9.9/32"]}},
                 "destination": {"all_destinations": True}},
            ],
            "deny_rules": [],
        }
    },
    "egress": {"network_access": {"restriction_mode": "FULL_ACCESS"}},
}


def test_hcl_has_resource_block_and_tf_safe_name():
    hcl = terraform.network_policy_hcl(_POLICY)
    assert 'resource "databricks_account_network_policy" "my_acl" {' in hcl  # '-' -> '_'
    assert hcl.rstrip().endswith("}")


def test_hcl_renders_nested_blocks_and_lists():
    hcl = terraform.network_policy_hcl(_POLICY)
    assert "ingress {" in hcl and "public_access {" in hcl and "allow_rules {" in hcl
    assert 'restriction_mode = "RESTRICTED_ACCESS"' in hcl
    assert 'ip_ranges = ["8.8.8.8/32", "9.9.9.9/32"]' in hcl
    assert "all_destinations = true" in hcl  # bool -> unquoted
    assert "egress {" in hcl and 'restriction_mode = "FULL_ACCESS"' in hcl


def test_hcl_omits_account_id_and_empty_lists():
    hcl = terraform.network_policy_hcl(_POLICY)
    assert "acc-123" not in hcl          # account_id dropped (provider supplies it)
    assert "deny_rules" not in hcl       # empty list omitted


def test_hcl_tf_name_falls_back_when_id_not_identifier():
    # a purely-numeric id can't start a TF identifier -> prefixed
    hcl = terraform.network_policy_hcl({"network_policy_id": "123"})
    assert 'resource "databricks_account_network_policy" "np_123" {' in hcl
