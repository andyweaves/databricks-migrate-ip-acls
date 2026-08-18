"""Shared Rich console, theme, and rendering helpers.

Everything the CLI prints goes through here so the look stays consistent: a single themed
`console`, plus helpers for the recurring shapes — a decisions/config panel, a pandas DataFrame as a
Rich table (row-capped for terminal readability), a syntax-highlighted JSON preview, and the
severity banners (info / warn / danger / success) the notebooks emitted as emoji prints.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any

import pandas as pd
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# One theme, referenced everywhere by semantic name rather than raw colour.
THEME = Theme(
    {
        "brand": "bold #FF3621",  # Databricks red
        "info": "cyan",
        "muted": "dim",
        "ok": "bold green",
        "warn": "bold yellow",
        "danger": "bold red",
        "heading": "bold white",
        "key": "bold cyan",
        "value": "white",
        "enforce": "bold red",
        "dry_run": "bold green",
    }
)

console = Console(theme=THEME, highlight=False)

# Default cap on rows rendered to the terminal; full data can be written out with --output.
MAX_TABLE_ROWS = 100


def banner(kind: str, message: str) -> None:
    """Print a one-line severity banner. kind in {info, warn, danger, success}."""
    glyphs = {"info": ("ℹ️ ", "info"), "warn": ("⚠️ ", "warn"),
              "danger": ("⛔ ", "danger"), "success": ("✅ ", "ok")}
    glyph, style = glyphs.get(kind, ("", "value"))
    console.print(Text(f"{glyph}{message}", style=style))


def rule(title: str) -> None:
    """A titled horizontal rule to separate sections."""
    console.rule(f"[heading]{title}[/heading]", style="brand")


def title_panel(title: str, subtitle: str | None = None) -> None:
    """The banner shown at the top of a command run."""
    body = Text(title, style="brand")
    if subtitle:
        body.append(f"\n{subtitle}", style="muted")
    console.print(Panel(body, border_style="brand", expand=False))


def workspace_panel(profile: str, host: str, workspace_id: Any) -> None:
    """A prominent panel naming the workspace this run will read from and act on (profile / URL /
    id), so the user is never in doubt about the target before analysis or any write."""
    body = Text()
    body.append("This run will analyse and (if you apply) modify:\n\n", style="heading")
    for label, value in (("profile      ", profile), ("workspace URL", host),
                         ("workspace id ", workspace_id)):
        body.append(f"  {label}  ", style="key")
        body.append(f"{value}\n", style="value")
    console.print(Panel(body, title="[brand]Target workspace[/brand]", border_style="brand",
                        expand=False))


def decisions_panel(title: str, rows: list[tuple[str, Any, str]]) -> None:
    """Render the run's configuration as a key / value / meaning table inside a panel — the CLI
    equivalent of the notebooks' `_decisions` DataFrame."""
    table = Table(show_header=True, header_style="heading", box=None, pad_edge=False, expand=True)
    table.add_column("Setting", style="key", no_wrap=True)
    table.add_column("Value", style="value")
    table.add_column("Meaning", style="muted")
    for name, value, meaning in rows:
        # Show the dash form (matching the actual CLI flags) so a copied name works as `--<name>`.
        table.add_row(name.replace("_", "-"), _fmt_value(value), meaning)
    console.print(Panel(table, title=f"[heading]{title}[/heading]", border_style="info"))


def _fmt_value(value: Any) -> str:
    if isinstance(value, bool):
        return "[ok]true[/ok]" if value else "[muted]false[/muted]"
    if value is None or value == "":
        return "[muted](unset)[/muted]"
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value) if value else "[muted](none)[/muted]"
    return str(value)


def dataframe(df: pd.DataFrame, title: str, max_rows: int = MAX_TABLE_ROWS,
              highlight_col: str | None = None) -> None:
    """Render a pandas DataFrame as a Rich table, capped to `max_rows`. If `highlight_col` is given
    and truthy for a row, that row is styled as a warning (used for the threat-match table)."""
    if df is None or df.empty:
        console.print(f"[muted]{title}: (no rows)[/muted]")
        return
    table = Table(title=f"[heading]{title}[/heading]", header_style="heading",
                  title_style="heading", show_lines=False, expand=False)
    for col in df.columns:
        table.add_column(str(col), overflow="fold")
    shown = df.head(max_rows)
    for _, row in shown.iterrows():
        style = "warn" if (highlight_col and row.get(highlight_col)) else None
        table.add_row(*[_cell(v) for v in row], style=style)
    console.print(table)
    if len(df) > max_rows:
        console.print(f"[muted]… showing {max_rows:,} of {len(df):,} rows "
                      f"(use --output to write the full result).[/muted]")


def _cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    if hasattr(value, "tolist"):  # numpy array
        return ", ".join(str(v) for v in value.tolist())
    return str(value)


def json_panel(title: str, obj: Any) -> None:
    """Syntax-highlighted JSON preview of a policy block (nothing is sent — preview only)."""
    console.print(Panel(JSON(json.dumps(obj)), title=f"[heading]{title}[/heading]",
                        border_style="info", expand=False))


@contextmanager
def status(message: str):
    """A spinner for a long step (feed download, SQL query, RDAP sweep)."""
    with console.status(f"[info]{message}[/info]", spinner="dots"):
        yield


def mode_banner(policy_mode: str) -> None:
    """The prominent dry_run vs enforce banner shown before a preview/apply."""
    if policy_mode == "enforce":
        console.print(Panel(
            Text("MODE = ENFORCE — non-matching traffic will be BLOCKED once applied. "
                 "Validate in dry_run first.", style="enforce"),
            border_style="danger", expand=False))
    else:
        console.print(Panel(
            Text("MODE = DRY_RUN — log-only; nothing is blocked.", style="dry_run"),
            border_style="ok", expand=False))


def responsibility_warning(direction: str) -> None:
    """Shown after the policy JSON preview on every run — including propose-only, since the printed
    JSON can be copied and used to create a policy elsewhere. `direction` names what the rules are
    built from, e.g. 'source IP addresses' (ingress) or 'FQDNs and storage destinations' (egress)."""
    body = Text()
    body.append("⚠️  THIS IS A SECURITY-ENFORCING NETWORK POLICY\n\n", style="warn")
    body.append(
        f"A network policy controls access to/from your Databricks environment. The {direction} "
        "above were derived from observed traffic and enrichment feeds as a best-effort starting "
        "point — they are ", style="value")
    body.append("not guaranteed to be complete or correct", style="danger")
    body.append(
        ".\n\nYou are solely responsible for reviewing every entry and confirming it is accurate and "
        "appropriate before using it in a policy — whether you create it here or copy this JSON to "
        "create it elsewhere. An incorrect or incomplete allow-list can block legitimate users or "
        "workloads (in enforce mode) or fail to block malicious ones.", style="value")
    console.print(Panel(body, title="[danger]Your responsibility[/danger]",
                        border_style="danger", expand=False))
