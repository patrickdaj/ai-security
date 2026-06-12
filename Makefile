.PHONY: help setup smoke lint test pipeline scan tf-fmt tf-validate lab-up lab-down

help:
	@echo "Targets:"
	@echo "  setup        Install the project (editable, with dev extras)"
	@echo "  smoke        Run the AI-layer smoke test (needs a backend/key)"
	@echo "  lint         Ruff over aug/ and automation/"
	@echo "  test         Pytest"
	@echo "  pipeline     Run the headless scan+triage pipeline against ."
	@echo "  scan         Run the pipeline with aggregation only (no model/key)"
	@echo "  tf-fmt       terraform fmt -check -recursive"
	@echo "  tf-validate  Validate the Terraform modules"
	@echo "  lab-up       Start the intentionally-vulnerable lab targets (isolated)"
	@echo "  lab-down     Tear the lab down"

setup:
	pip install -e ".[dev]"

smoke:
	python -m aug.smoke

lint:
	ruff check aug automation

test:
	pytest -q

pipeline:
	python -m automation --target . --out scratch/pipeline -v

scan:
	python -m automation --target . --out scratch/pipeline --no-triage -v

tf-fmt:
	terraform fmt -check -recursive

tf-validate:
	@for d in terraform/automation modules/08-cloud-iac/project/terraform; do \
		echo "== $$d =="; \
		terraform -chdir=$$d init -backend=false -input=false >/dev/null && \
		terraform -chdir=$$d validate; \
	done

lab-up:
	docker compose -f labs/docker-compose.yml up -d

lab-down:
	docker compose -f labs/docker-compose.yml down
