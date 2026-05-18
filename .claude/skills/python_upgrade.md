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

### Native Extension Strategy
Python upgrades break native extensions (C, C++, Rust) because pre-built wheels are version-specific. There are two categories:

**Direct pins** — packages explicitly listed in `.in` files. Easy to spot and bump.

**Transitive deps** — packages pulled in by other packages. These are the hard ones. pip-compile/uv lock resolves metadata successfully, but install fails because the resolved version has no wheel for the target Python and the source build fails.

#### How to find all native extensions in a project
```sh
# List packages with C/Rust extensions in the current environment:
pip list --format=json | python -c "
import json, sys, importlib.metadata
for pkg in json.load(sys.stdin):
    dist = importlib.metadata.distribution(pkg['name'])
    # Packages with compiled code typically have .so/.pyd files
    if any(f.suffix in ('.so', '.pyd') for f in (dist.files or [])):
        print(f\"{pkg['name']}=={pkg['version']}\")
"
```
Or inspect the compiled .txt files for packages known to ship native code (look for keywords: binary, cffi, Cython, maturin, setuptools-rust in their build systems).

#### The iterative fix loop
Expect 1-3 rounds — this is normal, not a sign something is wrong:
1. Recompile requirements (this may succeed even if install will fail)
2. Attempt install
3. If install fails: read the error, identify the package and why it failed
4. Find the minimum version of that package with a wheel for the target Python (check PyPI files tab or `pip index versions PACKAGE`)
5. Add a floor pin in the appropriate `.in` file (e.g. `somepackage>=X.Y.Z`)
6. Go to step 1

#### Three failure modes to expect
| When it fails | What you see | Example cause |
|---|---|---|
| **Compile time** | pip-compile/uv lock error | Package has no valid metadata for target Python |
| **Install time** | `Failed building wheel` / `setup.py egg_info` error | No pre-built wheel; source build uses APIs removed in target Python |
| **Runtime** | `ModuleNotFoundError` / `ImportError` at startup | Package installs fine but uses stdlib modules or internal APIs removed in the target Python (e.g. `six.moves`, `cgi`, `imghdr`, private CPython APIs) |

For runtime failures: the package installed successfully but is too old to actually *run* on the target Python. The fix is the same — add a floor pin for a version that supports the target Python — but you won't discover these until you try to start the app or run tests.

**Why this happens:** pip-compile resolves dependency metadata without building wheels. A package can report valid metadata for any Python version while its actual wheel build fails. And even installable packages can break at runtime if they use removed stdlib modules or private interpreter APIs.

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
* **Scan for native extensions:** Use the method in the "Native Extension Strategy" section above to identify all C/Rust/compiled packages in the dependency tree. For each, check whether a wheel exists for the target Python on PyPI. Flag any that need version bumps.
* **Confirm Docker base image exists:** verify `python:X.Z-slim-bookworm` tag is published.
* **Ask the user:** "Would you like me to run the install commands for you, or will you run them manually?" Respect their preference for Steps 4-5.

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
* Bump direct pins in `.in` files (or `pyproject.toml`) for any native packages flagged in Step 2.
* For transitive native deps without target-Python wheels: add floor pins to the appropriate `.in` file. The minimum compatible version can be found on the package's PyPI "Download files" page (look for a wheel matching `cp3Z`).
* Follow the iterative fix loop described in the "Native Extension Strategy" section. Expect recompile → install → fix cycles.
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
**Important:** Resolution succeeding does NOT mean install will succeed. Native extensions resolve metadata fine but fail when actually building wheels. Follow the iterative fix loop (recompile → install → read error → add floor pin → repeat) until install passes cleanly.

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
