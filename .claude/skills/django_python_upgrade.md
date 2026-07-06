---
name: django-python-upgrade-router
description: Router skill that delegates combined upgrade requests to python-upgrade and django-upgrade skills.
triggers:
  - django python upgrade
  - upgrade django and python
  - full runtime and framework upgrade
  - python and django migration
---

# OVERVIEW
Use one or both, depending on the request:
* Python runtime and tooling upgrade: see `.claude/skills/python_upgrade.md`
* Django framework and ecosystem upgrade: see `.claude/skills/django_upgrade.md`

# HOW TO RUN
1. If the request is only about changing Python versions (Docker/CI/pre-commit/runtime compatibility), run the Python skill.
2. If the request is only about changing Django/Wagtail versions and app compatibility, run the Django skill.
3. If both runtime and framework are changing, run Python first, then Django.