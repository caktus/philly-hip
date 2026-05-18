---
name: django-upgrade
description: Django framework upgrade workflow with Django/Wagtail compatibility checks, dependency pin updates, and migration validation.
triggers:
  - django upgrade
  - upgrade django
  - bump django version
  - django lts upgrade
  - wagtail compatibility upgrade
---

# OVERVIEW
You are executing a Django framework upgrade for this project. You have permission to read files, edit dependencies/configuration, and run terminal commands. Do not skip steps.

FIRST: Read this skill fully before acting. If this is a new/unfamiliar project, run Step 0 to discover project specifics, then execute Steps 1-6.

# PHILLY-HIP PROJECT REFERENCE (verified May 2026)
This section documents philly-hip. For other projects, run Step 0 and replace these facts.

* Stack: Django 5.2 LTS + Wagtail 7.x CMS
* Dependency management: pip-tools with requirements/base/, requirements/dev/, requirements/deploy/
* Recompile command: make update_requirements
* Install command: make install_requirements
* Test command: make run-tests (includes makemigrations --dry-run --check, then pytest)
* Settings under test: DJANGO_SETTINGS_MODULE=hip.settings.dev

### Django ecosystem packages to verify during upgrade
* wagtail
* wagtailmenus
* wagtail-modeladmin
* social-auth-app-django
* any Wagtail add-ons in requirements/base/base.in

# EXECUTION STEPS

## Step 0. Project Discovery (for unfamiliar projects)
If this is not philly-hip, or the reference is stale:
* Read README.md, requirements files, pytest.ini, and CI config.
* **Identify the dependency manager:** Look for `pyproject.toml` with `[tool.uv]` (uv project), `uv.lock` (uv lockfile), `requirements/*.in` files (pip-tools), or a Makefile with pip-compile commands.
* Identify current Django, Wagtail, and all first/third-party Django apps.
* Record test and migration commands used by the project.

### Dependency Manager Detection
| Indicator | Where Django pin lives | Recompile command | Install command |
|---|---|---|---|
| `pyproject.toml` with `[tool.uv]` or `uv.lock` | `pyproject.toml` `[project.dependencies]` | `uv lock` | `uv sync` |
| `requirements/*.in` + Makefile pip-compile | `requirements/base/base.in` | `make update_requirements` | `make install_requirements` |
| `requirements/*.in` + uv in Makefile | `requirements/base/base.in` | `make update_requirements` | `make install_requirements` |

## Step 1. Detect Current Version and Confirm Target
**Always start here.** Auto-detect the current Django (and Wagtail, if applicable) version from the dependency source:
* **pip-tools projects:** read `requirements/base/base.in`
* **uv projects:** read `pyproject.toml` `[project.dependencies]`

Report clearly to the user:

> **Current Django version: X.Y** (detected from requirements/base/base.in)
> **Current Wagtail version: X.Y** (if applicable)

If the user has not specified a target version, ask:
> Which Django version would you like to upgrade to? (LTS versions recommended: 4.2, 5.2, 6.2, ...)

If they have specified one, confirm:
> **Upgrading: Django X.Y → Django X.Z**

Do not proceed until the current and target versions are both confirmed.

## Step 2. Pre-flight Compatibility Checks
Before editing any dependency files:
* **Check Django/Python compatibility matrix:** https://docs.djangoproject.com/en/stable/faq/install/#what-python-version-can-i-use-with-django — confirm the project's current Python version supports the target Django.
* **Check Wagtail compatibility with target Django:** https://docs.wagtail.org/en/stable/releases/ — confirm Wagtail has a release supporting the target Django. If not, identify the required Wagtail upgrade.
* **Check ecosystem package compatibility:** For each package in the "Django ecosystem packages" table, verify it supports the target Django version (check PyPI classifiers or changelogs). Flag any that need pin bumps or replacements.
* **Review Django release notes for breaking changes:** Read the "Backwards incompatible changes" and "Features deprecated" sections for each version between current and target.

If any pre-flight check reveals a hard blocker (e.g., Wagtail doesn't support the target Django yet), report the blocker and stop. Do not partially upgrade.

## Step 3. Dependency Pin Updates
* Update Django, Wagtail, and ecosystem package pins:
  * **pip-tools:** edit `.in` files
  * **uv projects:** edit `pyproject.toml` `[project.dependencies]`
* Keep related packages coherent (for example, djangorestframework, django-filter, and Wagtail extensions).
* Recompile/lock:

  **pip-tools projects:**
  ```sh
  make update_requirements
  ```

  **uv projects:**
  ```sh
  uv lock
  ```

* If compilation/locking fails, iterate pins until a solvable set is found. Note: pip-compile/uv header lines in .txt/.lock files update automatically — no manual edit needed.

## Step 4. Install and Static Checks
* Sync environment:

  **pip-tools projects:**
  ```sh
  make install_requirements
  ```

  **uv projects:**
  ```sh
  uv sync
  ```

* Run migration consistency check:
  ```sh
  python manage.py makemigrations --dry-run --check
  ```
  (For uv projects, prefix with `uv run` if not in an activated venv.)
* If this fails, generate required migrations and include them in the upgrade.

## Step 5. Test and Runtime Verification
* Run full tests:
  ```sh
  make run-tests
  ```
* Fix framework-level breakages caused by deprecations, middleware/settings changes, admin API changes, model field behavior changes, or template tag incompatibilities.
* Pay special attention to Wagtail admin/editor flows and custom hooks.

## Step 6. Data and Schema Validation
* Ensure migrations apply cleanly and no model/schema drift remains.
* Investigate database column/type mismatches that surface after framework upgrades.
* Verify key content models render and save correctly in CMS workflows.

## Step 7. CI and Smoke Test
* Run CI test workflow or equivalent local checks used by CI.
* Smoke-test the site:
  ```sh
  python manage.py runserver
  ```
* Validate admin login, Wagtail pages, and critical public routes.
