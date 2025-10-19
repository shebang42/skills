# Python Development Skills Collection

Three focused, modular skills for professional Python development with Git and Docker.

## Skills Overview

### 1. python-dev
**Focus**: Python development with TDD, type safety, and code quality

**Use when**:
- Creating Python projects
- Implementing features with test-driven development
- Ensuring code quality with type hints and testing

**Key Features**:
- Test-Driven Development workflow (pytest + coverage.py)
- SOLID principles and OOP patterns
- Type safety with mypy
- Code quality with ruff (linting + formatting)
- Package management with uv
- 80+ percent test coverage requirement
- Pydantic validation
- Project initialization script

**Bundled Resources**:
- `scripts/init_project.py` - Initialize Python project structure
- Reference guides for TDD, testing patterns, configuration, documentation

### 2. gitea-workflow
**Focus**: Git workflow with Gitea integration using gitflow

**Use when**:
- Setting up Git repositories
- Creating repositories on Gitea server
- Managing feature/bugfix/release branches
- Following gitflow branching strategy

**Key Features**:
- Gitflow branching (main, develop, feature/, bugfix/, release/, hotfix/)
- Gitea API integration
- Conventional commit messages
- Pull request workflow
- **Secure**: Reads credentials from environment variables (no hardcoded secrets)

**Bundled Resources**:
- `scripts/init_repo.py` - Initialize Git and create Gitea repository
- `scripts/gitea_config.py` - Configuration loader from environment
- Reference guides for commit conventions, Gitea API

**Configuration Required**:
```bash
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-access-token]"
```

### 3. docker-dev
**Focus**: Docker containerization for development and deployment

**Use when**:
- Creating Dockerfiles
- Setting up docker compose
- Deploying applications with containers

**Key Features**:
- Multi-stage build templates
- Security best practices (non-root users, minimal images)
- docker compose orchestration
- Environment configuration with .env files
- Health checks and logging
- Development vs production configurations

**Bundled Resources**:
- Dockerfile template with multi-stage builds
- docker-compose.yml template with PostgreSQL
- .env.example template
- .dockerignore template
- Reference guides for Docker patterns, security, compose configurations

## Setup Instructions

### 1. Environment Variables for Gitea

To use the gitea-workflow skill, set up environment variables:

#### Option A: Shell Profile (Persistent)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Gitea Configuration
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-access-token]"
```

Then reload: `source ~/.bashrc`

#### Option B: Project .envrc (direnv)

Install direnv, then create `.envrc` in your workspace:

```bash
# Install direnv
sudo apt install direnv  # or: brew install direnv

# Add to shell profile
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# Create .envrc
cat > .envrc << 'EOF'
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-access-token]"
EOF

# Allow directory
direnv allow .
```

#### Option C: Manual Export (Temporary)

```bash
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-access-token]"
```

### 2. Verify Configuration

```bash
# Test Gitea configuration
python -c "
from gitea_config import load_config
config = load_config()
print(f'Gitea URL: {config.url}')
print(f'Username: {config.username}')
print('Configuration loaded successfully!')
"
```

## Typical Workflow

### Starting a New Project

```bash
# 1. Create Python project structure
python python-dev/scripts/init_project.py my-project

cd my-project

# 2. Initialize Git and create Gitea repository
python ../gitea-workflow/scripts/init_repo.py my-project

# 3. Set up Docker
cp ../docker-dev/assets/Dockerfile.template Dockerfile
cp ../docker-dev/assets/docker-compose.yml.template docker-compose.yml
cp ../docker-dev/assets/env.example.template .env.example
cp .env.example .env

# Edit Dockerfile to replace package_name
# Edit docker-compose.yml to customize services
# Edit .env with your configuration

# 4. Start development with TDD
uv run pytest  # Run tests
uv run ruff format .  # Format code
uv run mypy src/  # Type check

# 5. Develop features
git checkout -b feature/my-feature
# Write test, write code, commit
git commit -m "feat: add new feature"
git push -u origin feature/my-feature

# 6. Deploy with Docker
docker compose up -d
```

## Skill Interactions

These skills work together seamlessly:

```
┌─────────────┐
│ python-dev  │ ──> Creates project structure
└──────┬──────┘      Initializes uv, pytest, mypy
       │
       │ Project ready for Git
       │
       ▼
┌─────────────┐
│gitea-workflow│ ──> Initializes Git repository
└──────┬──────┘      Creates Gitea remote
       │              Sets up gitflow branches
       │
       │ Repository initialized
       │
       ▼
┌─────────────┐
│ docker-dev  │ ──> Adds containerization
└─────────────┘      Provides deployment config
                     Security best practices
```

Each skill is **independent** and **modular**:
- Use python-dev alone for local Python development
- Use gitea-workflow for any project needing Git/Gitea integration
- Use docker-dev for any project needing containerization
- Use all three together for complete development workflow


## Project Structure Example

After using all three skills:

```
my-project/
├── .git/                       # From gitea-workflow
├── .gitignore
├── Dockerfile                  # From docker-dev
├── docker-compose.yml          # From docker-dev
├── .dockerignore              # From docker-dev
├── .env.example               # From docker-dev
├── .env                       # Your configuration
├── pyproject.toml             # From python-dev
├── uv.lock                    # From python-dev
├── README.md
├── ARCHITECTURE.md
├── PLANNING.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       └── repositories/
└── tests/
    ├── __init__.py
    ├── test_models/
    └── test_services/
```

## Quick Command Reference

### Python Development
```bash
uv sync --dev                  # Install dependencies
uv run pytest                  # Run tests
uv run pytest --cov=src        # Run with coverage
uv run ruff format .           # Format code
uv run ruff check .            # Lint code
uv run mypy src/               # Type check
```

### Git Workflow
```bash
git checkout -b feature/name   # Start feature
git commit -m "feat: ..."      # Commit with convention
git push -u origin feature/name # Push feature
# Create PR on Gitea web UI
```

### Docker
```bash
docker compose build           # Build images
docker compose up -d           # Start services
docker compose logs -f app     # View logs
docker compose exec app bash   # Execute command
docker compose down            # Stop services
```

## Documentation

Each skill includes comprehensive documentation:

- **SKILL.md** - Main skill guide with quick start and examples
- **references/** - Detailed guides for specific topics
- **scripts/** - Automation scripts
- **assets/** - Templates and resources

## Requirements

- Python 3.13
- uv (package manager)
- Git
- Docker and docker compose
- Access to Gitea server (for gitea-workflow)
