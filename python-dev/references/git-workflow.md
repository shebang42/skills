# Git Workflow Guide

## Gitea Configuration

**Server details are read from environment variables:**
- `GITEA_URL` - Gitea server URL (e.g., https://git.home:3443)
- `GITEA_USERNAME` - Your Gitea username
- `GITEA_TOKEN` - Your Gitea access token

Set these in `~/.config/python-dev/config` or as environment variables.

## Gitflow Workflow

### Branch Structure

- **main** - Production-ready code (NOT "master")
- **develop** - Integration branch for features
- **feature/** - Feature branches (e.g., `feature/user-authentication`)
- **bugfix/** - Bug fix branches (e.g., `bugfix/fix-login-error`)
- **hotfix/** - Emergency fixes for production

### Creating a New Project Repository

```bash
# Create repository on Gitea using API (uses environment variables)
curl -X POST "${GITEA_URL}/api/v1/user/repos" \
  -H "Authorization: token ${GITEA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "project-name",
    "description": "Project description",
    "private": false,
    "auto_init": false
  }'

# Initialize local repository
git init
git branch -M main
git remote add origin ${GITEA_URL}/${GITEA_USERNAME}/project-name.git

# Create develop branch
git checkout -b develop
git push -u origin develop

# Push main branch
git checkout main
git push -u origin main

# Set develop as default working branch
git checkout develop
```

### Feature Development Workflow

```bash
# Start from develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "feat: implement feature functionality"

# Push feature branch
git push -u origin feature/feature-name

# When feature is complete, create pull request via Gitea web UI
# After review and approval, merge to develop
```

### Commit Message Convention

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks (dependencies, build config)
- `perf`: Performance improvements

**Examples:**
```
feat(auth): add JWT token validation

Implement token validation middleware with expiration checking
and signature verification.

Closes #123
```

```
fix(api): handle null response from external service

Add null check and default value when external API returns null.
```

### Pull Request Process

1. **Create PR** - Use Gitea web interface to create PR from feature to develop
2. **Review** - Code review required before merge
3. **Tests** - All tests must pass
4. **Merge** - Squash and merge or merge commit (no fast-forward for traceability)
5. **Delete branch** - Remove feature branch after merge

### Release Process

```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Finalize version, update CHANGELOG, etc.
git commit -m "chore: prepare release v1.0.0"

# Merge to main
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.0.0
git push origin develop

# Delete release branch
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### Hotfix Workflow

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix

# Fix the issue
git commit -m "fix: resolve critical production bug"

# Merge to main
git checkout main
git merge --no-ff hotfix/critical-bug-fix
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff hotfix/critical-bug-fix
git push origin develop

# Delete hotfix branch
git branch -d hotfix/critical-bug-fix
```

## Branch Protection Rules

Configure in Gitea repository settings:

- **main branch:**
  - Require pull request reviews (at least 1 approval)
  - Require status checks to pass
  - Prevent direct pushes
  - Prevent force pushes

- **develop branch:**
  - Require pull request reviews for major changes
  - Allow direct pushes for minor updates (with caution)

## .gitignore Template

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.*.local

# uv
.uv/

# Docker
*.log
docker-compose.override.yml

# Project specific
*.db
*.sqlite3
local_settings.py
```

## Best Practices

1. **Never commit secrets** - Use .env files and environment variables
2. **Commit frequently** - Small, logical commits are easier to review and revert
3. **Write clear messages** - Follow conventional commits format
4. **Keep branches short-lived** - Merge features within days, not weeks
5. **Sync regularly** - Pull from develop frequently to avoid merge conflicts
6. **Review own code** - Review your changes before creating PR
7. **Clean history** - Squash commits if needed to maintain clean history
8. **Tag releases** - Use semantic versioning (v1.2.3)
