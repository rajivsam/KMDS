# KMDS Workspace Initialization

## Project Overview
KMDS is a knowledge management toolkit for data science teams. It captures experimental context, decision rationale, and project metadata as structured knowledge graphs, with CLI entrypoints and optional local LLM integrations.

## Key Project Files
- `README.md` — primary project overview and usage guide
- `pyproject.toml` — package metadata, dependencies, and CLI script definitions
- `src/kmds/` — main package source code
- `tests/` — unit and integration tests for core functionality
- `docs/` — documentation source and build artifacts
- `high_level_reports/` — existing business and design report artifacts

## Main CLI Commands
Defined in `pyproject.toml` under `[project.scripts]`:
- `kmds-summary-log`
- `kmds-exec-summary`
- `kmds-search`
- `kmds-ask`
- `kmds-observe`

## Development Environment
- OS: Linux
- Python: `>=3.12`
- Virtual environment: `.venv/`
- Install dependencies via `pip install -e .` or `pip install -r requirements.txt`

## Relevant Source Areas
- `src/kmds/cli/` — CLI entrypoints and argument handling
- `src/kmds/ontology/` — ontology and graph generation logic
- `src/kmds/search/` — semantic search and orchestration
- `src/kmds/utils/` — shared utilities and helpers

## Initialization Guidance
Use this file as the starting reference for future iterations. When working next:
1. Confirm package structure in `src/kmds/`
2. Review CLI scripts and tests for the feature area being changed
3. Keep changes focused and document new behavior in `README.md`, `docs/`, or `high_level_reports/` as appropriate

## Notes for Copilot
- Prioritize reproducible CLI workflows and test coverage
- Keep modifications aligned with the repository's data science knowledge management domain
- Use `pyproject.toml` as the canonical source for package and entrypoint details
