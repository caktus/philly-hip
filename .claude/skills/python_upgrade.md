---
name: python-upgrade
description: Generic Python runtime upgrade workflow for projects using Docker, CI, pip-tools or uv, and compiled dependencies.
triggers:
  - python upgrade
  - upgrade python
  - bump python version
  - update runtime to python
  - python version migration
---

# OVERVIEW
You are executing a Python runtime upgrade for this project. You have permission to read files, edit configurations, and run terminal commands. Do not skip steps.

FIRST: Read this skill fully before acting. If this is a new/unfamiliar project, run Step 0 to discover project specifics, then execute Steps 1-5.

# PHILLY-HIP PROJECT REFERENCE (verified May 2026)
This section documents philly-hip. For other projects, run Step 0 and replace these facts.

* Stack: Python + Django/Wagtail app, PostgreSQL 15, Node 20 frontend build
* Requirements: pip-tools (*.in -> *.txt), split into requirements/base/, requirements/dev/, requirements/deploy/
* Recompile command: make update_requirements
* Install command: make install_requirements
* Test command: make run-tests
* Local env: direnv with layout python /opt/homebrew/bin/python3.X in .envrc
* Deploy: Docker -> AWS ECR -> EKS, uwsgi
* CI: .github/workflows/test.yml

### Files containing a Python version string (must all be updated)
| File | What to change | Example |
|---|---|---|
| Dockerfile | FROM python:X.Y-slim-bookworm | python:3.13-slim-bookworm |
| .github/workflows/test.yml | python-version: 'X.Y' | python-version: '3.13' |
| .pre-commit-config.yaml | language_version: python3.X (black hook) | language_version: python3.13 |
| README.md | Python >= 3.X prerequisites | Python >= 3.13 |
| .envrc | layout python /opt/homebrew/bin/python3.X | local dev only, not committed |
| requirements/deploy/deploy.in | uwsgi pin comment mentioning Python version | update comment |
| requirements/deploy/deploy.txt | pip-compile header | regenerate automatically |

### Compiled/native dependencies to watch
| Package | Current pin | Why it matters |
|---|---|---|
| psycopg2-binary | 2.9.9 | C extension; confirm wheel availability |
| libsass | 0.23.0 | C extension; can lag new Python support |
| cffi | 1.17.1 | C extension; cryptography dependency |
| uwsgi | 2.0.26 | C extension; deploy-only and often fragile |
| Pillow | transitive | C extension; verify support |

# EXECUTION STEPS

## Step 0. Project Discovery (for unfamiliar projects)
If this is not philly-hip, or the reference is stale:
* Read README.md, Makefile, Dockerfile, CI config, and requirement files.
* **Identify the dependency manager:** Look for `pyproject.toml` with `[tool.uv]` (uv project), `uv.lock` (uv lockfile), `requirements/*.in` files (pip-tools), or a Makefile with pip-compile commands. Record which tool manages dependencies.
* Identify requirement file layout, test command, deploy toolchain, and every Python version string location.
* Update the reference section in this skill before continuing.

### Dependency Manager Detection
| Indicator | Manager | Recompile command | Install command |
|---|---|---|---|
| `pyproject.toml` with `[tool.uv]` or `uv.lock` | uv | `uv lock` | `uv sync` |
| `pyproject.toml` with `[project]` only | uv (or pip-tools) | `uv lock` or `uv pip compile` | `uv sync` or `uv pip sync` |
| `requirements/*.in` + Makefile pip-compile | pip-tools | `make update_requirements` | `make install_requirements` |
| `requirements/*.in` + uv in Makefile | uv as pip-tools backend | `make update_requirements` (uses `uv pip compile`) | `make install_requirements` (uses `uv pip sync`) |

## Step 1. Detect Current Version and Confirm Target
**Always start here.** Auto-detect the current Python version from project files (Dockerfile FROM line is the source of truth). Report it clearly to the user:

> **Current Python version: X.Y** (detected from Dockerfile / CI / requirements headers)

If the user has not specified a target version, ask:
> Which Python version would you like to upgrade to?

If they have specified one, confirm:
> **Upgrading: Python X.Y → Python X.Z**

Do not proceed until the current and target versions are both confirmed.

## Step 2. Pre-flight Checks
Before editing any files:
* **Verify target Python is installed locally:** run `python3.Z --version`. If missing, tell the user to install it first (e.g. `brew install python@3.Z` or `uv python install 3.Z`) and stop.
* **Check compiled/native dependency support:** For each package in the "Compiled/native dependencies to watch" table, verify wheels exist for the target Python on PyPI (check https://pypi.org/project/PACKAGE/#files or run `pip index versions PACKAGE`). Flag any package that lacks target-version support — these need pin bumps or replacements before proceeding.
* **Confirm Docker base image exists:** verify `python:X.Z-slim-bookworm` tag is published.

If any pre-flight check fails, report the blocker and stop. Do not partially upgrade.

## Step 3. Infrastructure Version Updates
Update the Python version in every file listed in the reference table above.
* Update Dockerfile base image tag.
* Update GitHub Actions python-version.
* Update pre-commit language_version for black.
* Update README prerequisites.
* Do not edit .envrc in-repo if ignored; explicitly tell the user what to change locally.
* Update version-related comments in deploy requirement input files.
* **If uv project (`pyproject.toml`):** update `requires-python` field (e.g. `requires-python = ">=3.13"`).
* Note: pip-compile/uv header lines in .txt/.lock files will update automatically during recompilation — no manual edit needed.

## Step 4. Dependency Resolution
* Bump pins in relevant .in files (or `pyproject.toml` dependencies) for any packages flagged in Step 2.
* Recompile/lock requirement files:

  **pip-tools projects:**
  ```sh
  make update_requirements
  ```

  **uv projects (pyproject.toml + uv.lock):**
  ```sh
  uv lock
  ```

  **uv as pip-tools backend (requirements/*.in):**
  ```sh
  uv pip compile requirements/base/base.in -o requirements/base/base.txt
  uv pip compile requirements/dev/dev.in -o requirements/dev/dev.txt
  uv pip compile requirements/deploy/deploy.in -o requirements/deploy/deploy.txt
  ```
  Or if the Makefile wraps this: `make update_requirements`

* If compilation/locking fails, resolve the failing package first (check error output for incompatible version constraints), then re-run.

## Step 5. Environment Rebuild and Test
* Recreate local environment:

  **pip-tools / direnv projects:**
  ```sh
  direnv allow
  make install_requirements
  ```

  **uv projects:**
  ```sh
  uv sync
  ```

* Rebuild Docker image if used for local test:
  ```sh
  docker compose build
  ```
* Run test suite:
  ```sh
  make run-tests
  ```
* Fix runtime-compatibility errors from stdlib removals/deprecations (for example, imghdr removal in 3.13, cgi module removal in 3.13).

## Step 6. Validation and CI
* Verify deploy image build:
  ```sh
  inv image.build
  ```
* Push branch and verify CI passes.
* Smoke-test locally with runserver if applicable.
