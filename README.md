# skills

A Python project scaffold.

## Overview

This repository contains Python code and tooling with a focus on quality, testing, type safety, and maintainability.

## Features

- **Testing**: `pytest`
- **Coverage**: `coverage.py`
- **Type checking**: `mypy`
- **Lint/format**: `ruff`
- **Env & packages**: `uv`
- **Containerization**: Docker and docker compose
- **Workflow**: Gitflow (feature branches from `develop`)

## Getting Started

- **Clone**
```bash
git clone <repo-url> skills
```

- **Set up environment with uv**
```bash
uv sync
```

## Development

- **Run tests**
```bash
uv run pytest -q
```

- **Coverage**
```bash
uv run coverage run -m pytest
uv run coverage report
# or generate HTML
uv run coverage html
```

- **Type check**
```bash
uv run mypy .
```

- **Lint & format**
```bash
uv run ruff format
uv run ruff check --fix
```

- **Docker**
```bash
docker compose up --build
```

## Contributing

- **Branching**: Create feature branches from `develop` using the `feature/` prefix.
- **PRs**: Open PRs to `develop`. Do not commit secrets.

## License

This project is licensed under the MIT License. See `LICENSE`.
