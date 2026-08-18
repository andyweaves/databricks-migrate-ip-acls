"""Unit tests for the AclConfig dataclass + input-combination validation."""

from __future__ import annotations

import pytest

from dbx_migrate_ip_acls.config import (
    AclConfig,
    validate_acl_apply,
    validate_disable_ip_acls,
)


def test_policy_mode_target_maps_to_block():
    assert AclConfig(policy_mode="dry_run").policy_mode_target == "ingress_dry_run"
    assert AclConfig(policy_mode="enforce").policy_mode_target == "ingress"


def test_defaults():
    cfg = AclConfig()
    assert cfg.policy_mode == "enforce"
    assert cfg.policy_name == ""
    assert cfg.auto_assign is True
    assert cfg.create_policy is False
    assert cfg.disable_existing_ip_acls is False
    assert cfg.export == ""


def test_validate_disable_ip_acls_noop_when_disabled():
    # not requested — never validated, regardless of create/assign.
    validate_disable_ip_acls(False, create_policy=False, auto_assign=False)


def test_validate_disable_ip_acls_requires_create_and_assign():
    for create, assign in ((True, False), (False, True), (False, False)):
        with pytest.raises(ValueError, match="creates AND assigns"):
            validate_disable_ip_acls(True, create_policy=create, auto_assign=assign)


def test_validate_disable_ip_acls_ok_with_create_and_assign():
    validate_disable_ip_acls(True, create_policy=True, auto_assign=True)


def test_validate_acl_apply_rejects_assign_without_create():
    with pytest.raises(ValueError, match="auto-assign"):
        validate_acl_apply(create_policy=False, auto_assign=True,
                           disable_existing_ip_acls=False, policy_mode="enforce")


def test_validate_acl_apply_rejects_dry_run_disable():
    with pytest.raises(ValueError, match="dry_run"):
        validate_acl_apply(create_policy=True, auto_assign=True,
                           disable_existing_ip_acls=True, policy_mode="dry_run")


def test_validate_acl_apply_rejects_disable_without_create_assign():
    with pytest.raises(ValueError, match="creates AND assigns"):
        validate_acl_apply(create_policy=False, auto_assign=False,
                           disable_existing_ip_acls=True, policy_mode="enforce")


def test_validate_acl_apply_ok_defaults():
    # create + assign + enforce, no disable — the default happy path.
    validate_acl_apply(create_policy=True, auto_assign=True,
                       disable_existing_ip_acls=False, policy_mode="enforce")
    # valid propose-only combo.
    validate_acl_apply(create_policy=False, auto_assign=False,
                       disable_existing_ip_acls=False, policy_mode="enforce")
