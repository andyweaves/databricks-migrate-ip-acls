"""dbx-migrate-ip-acls — migrate a Databricks workspace's IP access list into a CBI policy.

A focused CLI that recreates this workspace's existing IP access list (ALLOW→allow rules,
BLOCK→deny rules) as a context-based ingress (CBI) account network policy, verbatim — no traffic
analysis, no enrichment — with account-level pre-checks and a dry-run-first, review-gated apply path.

Extracted from databricks-network-policy-helper (which retains the traffic-analysis `ingress` /
`egress` commands).
"""

__version__ = "0.1.0"
