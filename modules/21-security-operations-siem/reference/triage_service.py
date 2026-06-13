"""REFERENCE — alert-triage webhook service (worked answer).

A SOAR (n8n/Shuffle/Tines) POSTs an alert; this returns the typed Triage so the
workflow can route on `verdict`. Reuses the shared aug triage engine.

    python triage_service.py
"""

from __future__ import annotations

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(message)s")
_client = AugClient()


def _to_finding(alert: dict) -> Finding:
    try:
        sev = Severity(alert.get("severity", "medium"))
    except ValueError:
        sev = Severity.medium
    return Finding(
        tool=alert.get("tool", "siem"),
        rule_id=alert.get("rule_id", "?"),
        title=(alert.get("title") or alert.get("rule_id", ""))[:120],
        severity=sev,
        location=alert.get("location", alert.get("host", "?")),
        description=alert.get("description", ""),
        context=alert.get("context") or json.dumps(alert.get("events", alert))[:4000],
    )


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        try:
            alert = json.loads(self.rfile.read(length) or "{}")
        except json.JSONDecodeError:
            self.send_error(400, "invalid JSON")
            return
        finding = _to_finding(alert)
        triage = triage_finding(_client, finding)
        body = triage.model_dump(mode="json")
        logging.info("triaged %s -> %s (%.2f)", finding.rule_id, body["verdict"],
                     body["confidence"])
        payload = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):  # quiet default access logging
        pass


if __name__ == "__main__":
    print("triage service on :8088 (POST an alert as JSON)")
    HTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
