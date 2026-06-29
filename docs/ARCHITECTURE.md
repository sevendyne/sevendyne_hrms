# Sevendyne HRMS Documentation

## Quick Links

- [README](../README.md) — Getting started with Docker
- [CONTRIBUTING](../CONTRIBUTING.md) — Candidate evaluation workflow

## Architecture

| Domain Module       | Django App        | Description                          |
|---------------------|-------------------|--------------------------------------|
| `authentication/`   | `apps.user`       | Login, registration, roles           |
| `attendance/`       | `apps.employee`   | Attendance registers                 |
| `leave_tracker/`    | `apps.employee`   | Leave types and requests             |
| `payroll/`          | `apps.payroll`    | Salary and payroll items             |

Additional modules: `main`, `hrms`, `candidate`, `client`, `job`, `asset`.

## Settings

| Environment | Module                         |
|-------------|--------------------------------|
| Local       | `config.settings.local`        |
| Production  | `config.settings.production`   |

## Docker

- **Local:** `docker compose up` uses `compose/local/Dockerfile`
- **Production:** Build with `compose/production/Dockerfile` and deploy with your orchestrator

## Environment Variables

| Variable              | Description                    | Default (local)        |
|-----------------------|--------------------------------|------------------------|
| `DATABASE_URL`        | PostgreSQL connection string   | Docker internal URL    |
| `DJANGO_SECRET_KEY`   | Django secret key              | Dev-only default       |
| `DJANGO_SETTINGS_MODULE` | Settings module             | `config.settings.local`|
| `REDIS_HOST`          | Celery broker host             | `redis` (Docker)       |
| `EMAIL_BACKEND`       | Email backend class            | Console backend        |
