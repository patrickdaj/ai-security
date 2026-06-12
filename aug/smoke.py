"""Smoke test for the AI layer: `python -m aug.smoke`.

Runs one finding through the triage engine end to end. Confirms your API key
works, the model is reachable, and structured outputs parse. A deliberately
weak SQL-injection snippet should come back as a high-severity true positive
with a parameterized-query fix.
"""

from __future__ import annotations

from rich import print as rprint

from aug.client import AugClient
from aug.models import Finding, Severity
from aug.triage import triage_finding

EXAMPLE = Finding(
    tool="semgrep",
    rule_id="python.lang.security.audit.formatted-sql-query",
    title="Possible SQL injection via string formatting",
    severity=Severity.medium,
    location="app/db.py:42",
    description="User input concatenated into a SQL query.",
    context=(
        "def get_user(conn, username):\n"
        "    cur = conn.cursor()\n"
        "    cur.execute(\"SELECT * FROM users WHERE name = '%s'\" % username)\n"
        "    return cur.fetchone()\n"
    ),
)


def main() -> None:
    client = AugClient()
    rprint(f"[bold]Backend:[/bold] {client.backend}   [bold]Model:[/bold] {client.model}")
    rprint("[bold]Triaging example finding...[/bold]\n")
    t = triage_finding(client, EXAMPLE)
    rprint(t.model_dump())


if __name__ == "__main__":
    main()
