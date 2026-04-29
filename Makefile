SHELL := /bin/sh

BACKEND_DIR := be/backend
FRONTEND_DIR := fe
BACKEND_ENV := $(BACKEND_DIR)/.env
DB_FILE := $(BACKEND_DIR)/app.db

PYTHON ?= python3
NPM ?= npm
COMPOSE ?= docker compose

.PHONY: help install db-init backend frontend dev docker up down logs build clean

help:
	@printf "%s\n" "Targets:"
	@printf "%s\n" "  make install   - create be/backend/.env from be/backend/.env.example"
	@printf "%s\n" "  make frontend  - run the Vite frontend on http://localhost:3000"
	@printf "%s\n" "  make backend   - run the Flask backend on http://localhost:5000"
	@printf "%s\n" "  make dev       - run frontend and backend together locally"
	@printf "%s\n" "  make docker    - build and run both services with the root docker-compose.yml"
	@printf "%s\n" "  make down      - stop the Docker Compose stack"
	@printf "%s\n" "  make logs      - follow Docker Compose logs"

install:
	@if [ ! -f "$(BACKEND_ENV)" ]; then \
		cp "$(BACKEND_DIR)/.env.example" "$(BACKEND_ENV)"; \
		printf "%s\n" "Created $(BACKEND_ENV) from $(BACKEND_DIR)/.env.example"; \
	else \
		printf "%s\n" "$(BACKEND_ENV) already exists"; \
	fi

db-init:
	@if [ ! -s "$(DB_FILE)" ]; then \
		printf "%s\n" "Initializing SQLite database at $(DB_FILE)"; \
		sqlite3 "$(DB_FILE)" < "$(BACKEND_DIR)/seed/schema.sql"; \
		sqlite3 "$(DB_FILE)" < "$(BACKEND_DIR)/seed/jobs_seed.sql"; \
	fi

backend: db-init
	cd $(BACKEND_DIR) && $(PYTHON) app.py

frontend:
	@set -a; \
	if [ -f "$(BACKEND_ENV)" ]; then . "$(BACKEND_ENV)"; fi; \
	set +a; \
	cd $(FRONTEND_DIR) && VITE_API_URL=http://localhost:5000 VITE_API_TOKEN="$$APP_TOKEN" $(NPM) run dev -- --host 0.0.0.0

dev: db-init
	@set -a; \
	if [ -f "$(BACKEND_ENV)" ]; then . "$(BACKEND_ENV)"; fi; \
	set +a; \
	trap 'kill $$backend_pid $$frontend_pid 2>/dev/null' INT TERM EXIT; \
	(cd $(BACKEND_DIR) && $(PYTHON) app.py) & backend_pid=$$!; \
	(cd $(FRONTEND_DIR) && VITE_API_URL=http://localhost:5000 VITE_API_TOKEN="$$APP_TOKEN" $(NPM) run dev -- --host 0.0.0.0) & frontend_pid=$$!; \
	wait $$backend_pid $$frontend_pid

docker up:
	$(COMPOSE) -f docker-compose.yml up --build

down:
	$(COMPOSE) -f docker-compose.yml down

logs:
	$(COMPOSE) -f docker-compose.yml logs -f

build:
	cd $(FRONTEND_DIR) && $(NPM) run build

clean:
	$(COMPOSE) -f docker-compose.yml down -v
