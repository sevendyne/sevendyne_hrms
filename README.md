# Sevendyne Enterprise HRMS

![Build Status](https://img.shields.io/badge/tests-passing-success)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Django Version](https://img.shields.io/badge/django-5.0%20LTS-green)

A robust, enterprise-grade Human Resource Management System built with Python and Django. Designed for easy containerized deployment across any office infrastructure.

## Features

- **Authentication** — Role-based login for admins, HRMS clients, and employees
- **Attendance** — Check-in, check-out, and attendance registers
- **Payroll** — Salary slips and payroll item management
- **Leave Tracker** — Leave types, requests, and approval workflows
- **Recruitment** — Candidate and job portal modules

## Project Structure

```
sevendyne_hrms/
├── .github/workflows/     # CI/CD pipelines (pytest, linting)
├── apps/                  # Django domain apps
│   ├── authentication/    # → apps/user
│   ├── attendance/        # → apps/employee
│   ├── payroll/
│   └── leave_tracker/     # → apps/employee
├── config/                # Django settings (base, local, production)
├── compose/               # Docker files (local & production)
├── docs/                  # Documentation
├── requirements/          # Split dependencies
└── docker-compose.yml     # One-command local orchestration
```

## Getting Started

Ensure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

```bash
# Clone the repository
git clone https://github.com/sevendyne/sevendyne_hrms.git
cd sevendyne_hrms

# Spin up the entire infrastructure (App, DB, Redis)
docker compose up --build
```

On first start, migrations run automatically and demo accounts are seeded.

Navigate to **http://localhost:8000** to access the portal.

### Demo Credentials

| Role     | Username      | Password       |
|----------|---------------|----------------|
| Admin    | `admin`       | `admin`          |
| Client   | `hrmsclient1` | `password@123`   |
| Employee | `employee1`   | `password@123`   |

Login URL: http://localhost:8000/app/login/

### Manual Setup (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt

# Configure PostgreSQL and set DATABASE_URL, then:
python manage.py migrate
python manage.py loaddata countries states
python manage.py seed_demo_data
python manage.py runserver
```

## Development

```bash
# Run tests
pytest

# Lint
flake8 apps config
black --check apps config
```

## Contributing

We use this repository to discover engineering talent. See [CONTRIBUTING.md](CONTRIBUTING.md) for the evaluation workflow and PR standards.

## License

Proprietary — Sevendyne. Contact hr@sevendyne.com for licensing inquiries.
