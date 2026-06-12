.PHONY: help setup smoke lint test lab-up lab-down

help:
	@echo "Targets:"
	@echo "  setup     Create venv hint + install the aug library (editable)"
	@echo "  smoke     Run the AI-layer smoke test (needs ANTHROPIC_API_KEY)"
	@echo "  lint      Ruff over aug/"
	@echo "  test      Pytest"
	@echo "  lab-up    Start the intentionally-vulnerable lab targets (isolated)"
	@echo "  lab-down  Tear the lab down"

setup:
	pip install -e ".[dev]"

smoke:
	python -m aug.smoke

lint:
	ruff check aug

test:
	pytest -q

lab-up:
	docker compose -f labs/docker-compose.yml up -d

lab-down:
	docker compose -f labs/docker-compose.yml down
