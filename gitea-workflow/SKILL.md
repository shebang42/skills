---
name: gitea-workflow
description: Git workflow with Gitea integration using gitflow branching strategy. Use when initializing Git repositories, creating Gitea repos, managing branches with gitflow, or working with feature/bugfix/release branches. Reads Gitea credentials from environment variables for security. Enforces conventional commits and pull request workflow.
---

# Gitea Workflow

Git workflow management with Gitea server integration following gitflow branching strategy.

## Configuration

Set these environment variables for Gitea integration:

```bash
export GITEA_URL="https://[your-gitea-server]:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-access-token]"
```

Add to your shell profile (.bashrc, .zshrc) or create a `.envrc` file:

```bash
# .envrc (use with direnv)
export GITEA_URL="https://[your-gitea-server]:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-access-token]"
```

## Gitflow Branch Strategy

```
main (production)
  ├── develop (integration)
  │   ├── feature/user-auth
  │   ├── feature/api-endpoints
  │   └── bugfix/fix-validation
  ├── release/v1.0.0
  └── hotfix/critical-bug
```

### Branch Types

- **main** - Production-ready code (tagged releases)
- **develop** - Integration branch for features
- **feature/** - New features (from develop)
- **bugfix/** - Bug fixes (from develop)
- **release/** - Release preparation (from develop)
- **hotfix/** - Emergency production fixes (from main)

## Quick Start

### Initialize Repository with Gitea

Use the bundled script:

```bash
python scripts/init_repo.py project-name
```

This will:
1. Initialize local Git repository
2. Create Gitea repository via API
3. Set up main and develop branches
4. Configure remote
5. Make initial commit

### Manual Setup

```bash
# Initialize local repo
git init
git branch -M main

# Create develop branch
git checkout -b develop

# Add Gitea remote (uses env vars)
git remote add origin $GITEA_URL/$GITEA_USERNAME/project-name.git

# Initial commit
git add .
git commit -m "chore: initial commit"

# Push branches
git push -u origin develop
git push -u origin main
```

## Feature Development

### Start Feature

```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/feature-name

# Work on feature...
git add .
git commit -m "feat: add feature functionality"

# Push feature branch
git push -u origin feature/feature-name
```

### Commit Message Convention

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(auth): add JWT token validation

Implement token validation middleware with expiration
checking and signature verification.

Closes #123
```

```
fix(api): handle null response from external service

Add null check and default value when external API
returns null to prevent crashes.
```

See [references/commit-conventions.md](references/commit-conventions.md) for more examples.

### Finish Feature

```bash
# Push final changes
git push origin feature/feature-name

# Create pull request on Gitea (web UI)
# After approval, merge to develop
# Delete feature branch after merge
```

## Release Process

```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Finalize version, update CHANGELOG
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
```

## Hotfix Workflow

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# Fix the issue
git commit -m "fix: resolve critical production bug"

# Merge to main
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff hotfix/critical-bug
git push origin develop

# Delete hotfix branch
git branch -d hotfix/critical-bug
```

## Pull Request Workflow

1. **Create PR** - Use Gitea web interface
2. **Code Review** - At least one approval required
3. **Tests Pass** - All CI checks must pass
4. **Merge** - Use squash or merge commit (no fast-forward)
5. **Delete Branch** - Remove feature branch after merge

## Gitea API Integration

The bundled scripts use Gitea API for automation:

- Create repositories
- List repositories
- Manage pull requests
- Check CI status

All scripts read credentials from environment variables.

See [references/gitea-api.md](references/gitea-api.md) for API details.

## .gitignore

Standard .gitignore for Python projects:

```gitignore
# Python
__pycache__/
*.py[cod]
.Python
.venv/
dist/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Type checking
.mypy_cache/

# Environment
.env
.env.local

# Secrets - NEVER commit
*.key
*.pem
secrets/
```

## Best Practices

1. **Never commit secrets** - Use environment variables
2. **Commit frequently** - Small, logical commits
3. **Clear messages** - Follow conventional commits
4. **Short-lived branches** - Merge features within days
5. **Sync regularly** - Pull from develop often
6. **Review before PR** - Review your own changes first
7. **Delete merged branches** - Keep repository clean

## Security

- Credentials stored in environment variables
- API tokens never in code or configuration files
- .gitignore includes common secret patterns
- Scripts validate environment before use

## Bundled Resources

### Scripts
- **init_repo.py** - Initialize Git repo and create on Gitea
- **gitea_config.py** - Configuration loader (from environment)

### References
- **commit-conventions.md** - Detailed commit message guide
- **gitea-api.md** - Gitea API reference and examples

## Quick Reference

**Start Feature**: `git checkout -b feature/name` (from develop)

**Commit**: `git commit -m "feat(scope): description"`

**Release**: develop → release/vX.Y.Z → main (tagged) → develop

**Hotfix**: main → hotfix/name → main (tagged) → develop

**Environment**: Set GITEA_URL, GITEA_USERNAME, GITEA_TOKEN
