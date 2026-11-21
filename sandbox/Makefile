COMPOSE := docker compose
SCENARIO ?= scenarios/muse_fingerprint.yaml
RUNS ?= 5
PROFILE ?=

.PHONY: up down logs build smoke test-unit scenario profiles shell-runner

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d --build store telemetry

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f store telemetry

smoke:
	@curl -sf http://localhost:8080/health | grep -q '"status":"ok"'
	@curl -sf http://localhost:8090/health | grep -q '"status":"ok"'
	@echo "smoke ok"

test-unit:
	$(COMPOSE) run --rm --entrypoint pytest runner -q

profiles:
	$(COMPOSE) run --rm runner --list-profiles

scenario:
	$(COMPOSE) run --rm runner --scenario /app/$(SCENARIO) --runs $(RUNS) $(if $(PROFILE),--profile $(PROFILE),)

shell-runner:
	$(COMPOSE) run --rm --entrypoint sh runner
