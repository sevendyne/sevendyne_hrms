# Sevendyne HRMS — Documentation

Welcome to the Sevendyne Enterprise HRMS documentation. This project was **built over one year by a team of three engineers** in our **local office space**. We are sharing it openly so collaborators can run it, extend it, and help us ship more quality software. **Additional Sevendyne projects will be published here soon.**

## Documentation Index

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Domain modules, settings, environment variables |
| [DOCKER.md](DOCKER.md) | Plug-and-play Docker setup |
| [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) | Production-ready repository layout |
| [VISIBILITY.md](VISIBILITY.md) | How to promote the repo on GitHub and social channels |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | How to collaborate and get evaluated |
| [../README.md](../README.md) | Project storefront and quick start |

## Who This Is For

- **Companies** that want a containerized HRMS they can run on their own infrastructure
- **Developers** looking to contribute features, fix bugs, or demonstrate their skills
- **Candidates** who prefer showing work through PRs over traditional interviews

## Quick Start

```bash
git clone https://github.com/sevendyne/sevendyne_hrms.git
cd sevendyne_hrms
docker compose up --build
```

Then open http://localhost:8000 and log in with the [demo credentials](../README.md#demo-credentials).

## Get Involved

1. **[Star the repository](https://github.com/sevendyne/sevendyne_hrms)** — helps visibility (see [VISIBILITY.md](VISIBILITY.md))
2. Fork and read [CONTRIBUTING.md](../CONTRIBUTING.md)
3. Pick a `good-first-issue` or `candidate-challenge` label
4. Submit a PR — we review for quality, tests, and documentation

**License:** [MIT](../LICENSE) — free for personal and commercial use.

We are actively looking for collaborators. More repositories from the Sevendyne team are coming.
