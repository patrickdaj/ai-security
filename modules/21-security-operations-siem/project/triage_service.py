"""STUB — alert-triage webhook service (the AI judgment layer for SOAR).

Build a tiny HTTP endpoint that any SOAR (n8n, Shuffle, Tines) can POST an alert
to and get back a typed triage verdict. n8n then routes on the verdict. Reference
in ../reference/. Dependency-free (stdlib http.server) so it runs anywhere.

    python triage_service.py        # listens on :8088
    curl -s localhost:8088 -d '{"rule_id":"...","title":"...","severity":"high","context":"..."}'
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402

_client = AugClient()


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        # TODO: read the JSON alert body, normalize it into a Finding (map the
        # SIEM fields to tool/rule_id/title/severity/location/context), run
        # triage_finding(_client, finding), and write the Triage back as JSON.
        raise NotImplementedError("Build the alert -> Finding -> triage handler.")


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
