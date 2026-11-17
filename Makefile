.DEFAULT_GOAL := help
UV := ./scripts/uv.sh

.PHONY: help editor-install editor-dev editor-build editor-test core-sync core-test core-lint core-format core-check validate-sample check-system verify

help:
	@echo "SGD3DGS development commands"
	@echo "  make editor-install   Install pinned editor dependencies"
	@echo "  make editor-dev       Run the editor development server"
	@echo "  make editor-build     Build the production editor bundle"
	@echo "  make editor-test      Format/lint checks, type-check, and editor tests"
	@echo "  make core-sync        Create/sync the Python 3.12 environment"
	@echo "  make core-test        Run Python tests"
	@echo "  make core-lint        Run Ruff and mypy"
	@echo "  make core-format      Format Python code"
	@echo "  make core-check       Run Python lint and tests"
	@echo "  make validate-sample  Validate the example scene manifest"
	@echo "  make verify           Build/test both primary components"

editor-install:
	npm --prefix apps/editor ci

editor-dev:
	npm --prefix apps/editor run develop

editor-build:
	npm --prefix apps/editor run build

editor-test:
	npm --prefix apps/editor run fmt
	npm --prefix apps/editor run lint
	npm --prefix apps/editor run lint:locales
	npm --prefix apps/editor test

core-sync:
	$(UV) sync --all-packages --extra api

core-test:
	$(UV) run pytest

core-lint:
	$(UV) run ruff check services/core
	$(UV) run ruff format --check services/core
	$(UV) run mypy

core-format:
	$(UV) run ruff check --fix services/core
	$(UV) run ruff format services/core

core-check: core-lint core-test

validate-sample:
	$(UV) run sgd3dgs validate --check-files examples/minimal-scene/scene.json

check-system:
	./scripts/check_system.sh

verify: editor-test editor-build core-check validate-sample
