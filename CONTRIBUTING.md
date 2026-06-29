# Contributing to Sevendyne HRMS

We love community collaboration and use this repository to discover engineering talent for Sevendyne projects. If you are a candidate looking to collaborate, follow this workflow:

## The Evaluation Process

1. **Find an Issue:** Look at our GitHub Issues page labeled with `good-first-issue` or `candidate-challenge`.
2. **Fork & Branch:** Fork this repository and create a descriptive branch (e.g., `feature/attendance-api`).
3. **Follow Our Standards:**
   - Write automated tests for all new logic using `pytest-django`.
   - Ensure all code complies with PEP 8 standards (use `black` and `flake8`).
4. **Submit a Pull Request:** Open a PR against our `main` branch.

## Definition of Done for PRs

We treat engineering discipline with high priority. Your PR will only be reviewed if:

- The CI pipeline passes perfectly (0 linting errors, 100% test success).
- Database migrations are cleanly generated and optimized.
- Clear documentation is provided for any new APIs or methods.

## Local Development Setup

```bash
docker compose up --build
```

Or install dependencies manually:

```bash
pip install -r requirements/local.txt
export DJANGO_SETTINGS_MODULE=config.settings.local
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

## Code Style

- Format with `black`
- Lint with `flake8`
- Run `pytest` before opening a PR

## Questions?

Open a GitHub Discussion or reach out via the issue tracker.
