#!/usr/bin/env bash
# One-time Codespaces/devcontainer setup: install the curriculum package and the
# core scanners the aug pipeline uses. Module-specific tools (Ghidra, AFL++,
# Falco, nmap, ...) are installed per-module as you reach them — see each
# module's Resources section.
set -euo pipefail

echo "==> Installing the curriculum package (editable, with dev extras)"
pip install --upgrade pip
pip install -e ".[dev]"

echo "==> Installing core scanners (semgrep, trivy, gitleaks)"
pip install semgrep || echo "semgrep install failed (continue)"
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
  | sh -s -- -b /usr/local/bin || echo "trivy install failed (continue)"
curl -sfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh \
  | sh -s -- -b /usr/local/bin || echo "gitleaks install failed (continue)"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env — add your ANTHROPIC_API_KEY (or set AUG_BACKEND=ollama)."
fi

cat <<'MSG'

Ready. Quick start:
  make smoke      # exercise the AI layer (needs a key or a local Ollama)
  make scan       # run the pipeline with no model (aggregation only)
  make pipeline   # full scan + AI triage

Open a module's README (e.g. modules/00-foundations/README.md) and build in its
project/ directory. The reference/ holds the worked solution.
MSG
