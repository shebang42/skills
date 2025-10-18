#!/usr/bin/env python3
"""Initialize a new Python project with standard structure and configuration."""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import NoReturn


def load_gitea_config() -> dict[str, str] | None:
    """Load Gitea configuration from config file or environment variables."""
    # Try config file first
    config_file = Path.home() / ".config" / "python-dev" / "config"
    if config_file.exists():
        config = {}
        for line in config_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        
        if all(k in config for k in ["GITEA_URL", "GITEA_USERNAME", "GITEA_TOKEN"]):
            return config
    
    # Try environment variables
    gitea_url = os.getenv("GITEA_URL")
    gitea_username = os.getenv("GITEA_USERNAME")
    gitea_token = os.getenv("GITEA_TOKEN")
    
    if all([gitea_url, gitea_username, gitea_token]):
        return {
            "GITEA_URL": gitea_url,
            "GITEA_USERNAME": gitea_username,
            "GITEA_TOKEN": gitea_token,
        }
    
    return None


def run_command(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a shell command and handle errors."""
    try:
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def create_project_structure(project_path: Path, package_name: str) -> None:
    """Create the project directory structure."""
    # Main directories
    (project_path / "src" / package_name).mkdir(parents=True, exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)
    (project_path / "scripts").mkdir(exist_ok=True)
    (project_path / "docs").mkdir(exist_ok=True)
    
    # Subdirectories in package
    for subdir in ["models", "services", "repositories", "api", "utils"]:
        (project_path / "src" / package_name / subdir).mkdir(exist_ok=True)
        (project_path / "src" / package_name / subdir / "__init__.py").touch()
    
    # Test subdirectories
    for subdir in ["test_models", "test_services", "integration"]:
        (project_path / "tests" / subdir).mkdir(exist_ok=True)
        (project_path / "tests" / subdir / "__init__.py").touch()
    
    # Create __init__.py files
    (project_path / "src" / package_name / "__init__.py").touch()
    (project_path / "tests" / "__init__.py").touch()


def create_gitignore(project_path: Path) -> None:
    """Create .gitignore file."""
    gitignore_content = """# Python
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
"""
    (project_path / ".gitignore").write_text(gitignore_content)


def create_pyproject_toml(project_path: Path, project_name: str, package_name: str) -> None:
    """Create pyproject.toml configuration."""
    pyproject_content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.13"
authors = [
    {{ name = "Your Name", email = "your.email@example.com" }}
]
dependencies = [
    "pydantic>=2.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "mypy>=1.11.0",
    "ruff>=0.6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 80

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"
ignore_missing_imports = false

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "ARG",  # flake8-unused-arguments
    "SIM",  # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/**/*" = ["ARG"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
"""
    (project_path / "pyproject.toml").write_text(pyproject_content)


def create_main_file(project_path: Path, package_name: str) -> None:
    """Create main entry point."""
    main_content = f'''"""Main application entry point."""


def main() -> None:
    """Run the application."""
    print("Hello from {package_name}!")


if __name__ == "__main__":
    main()
'''
    (project_path / "src" / package_name / "main.py").write_text(main_content)


def create_example_test(project_path: Path, package_name: str) -> None:
    """Create an example test file."""
    test_content = f'''"""Example test file."""

import pytest


def test_example() -> None:
    """Example test that always passes."""
    assert True


def test_example_with_fixture(sample_data: dict[str, int]) -> None:
    """Example test using a fixture."""
    assert sample_data["value"] == 42


@pytest.fixture
def sample_data() -> dict[str, int]:
    """Provide sample data for tests."""
    return {{"value": 42}}
'''
    (project_path / "tests" / "test_example.py").write_text(test_content)


def create_planning_file(project_path: Path) -> None:
    """Create PLANNING.md file."""
    planning_content = """# Project Planning

## Task Breakdown

### Phase 1: Setup
- [x] Initialize project structure
- [x] Configure dependencies
- [ ] Set up Docker environment
- [ ] Create documentation

### Phase 2: Core Features
- [ ] Define domain models
- [ ] Implement business logic
- [ ] Create data access layer
- [ ] Build API layer

### Phase 3: Testing
- [ ] Unit tests for models
- [ ] Unit tests for services
- [ ] Integration tests
- [ ] Achieve 80%+ coverage

### Phase 4: Deployment
- [ ] Create Dockerfile
- [ ] Configure docker compose
- [ ] Set up CI/CD
- [ ] Deploy to production

## Current Status

Working on: Project initialization
Blocked by: None
Next up: Define domain models
"""
    (project_path / "PLANNING.md").write_text(planning_content)


def initialize_git(project_path: Path, repo_name: str) -> None:
    """Initialize git repository and create on Gitea."""
    # Initialize local git
    run_command(["git", "init"], cwd=project_path)
    run_command(["git", "branch", "-M", "main"], cwd=project_path)
    
    # Load Gitea configuration
    gitea_config = load_gitea_config()
    
    if not gitea_config:
        print("\nWarning: Gitea configuration not found.")
        print("To enable automatic repository creation, create:")
        print("  ~/.config/python-dev/config")
        print("\nWith the following content:")
        print("  GITEA_URL=https://git.home:3443")
        print("  GITEA_USERNAME=your-username")
        print("  GITEA_TOKEN=your-access-token")
        print("\nOr set environment variables: GITEA_URL, GITEA_USERNAME, GITEA_TOKEN")
        print("\nSkipping remote repository setup. You can add it manually later.")
        return
    
    gitea_url = gitea_config["GITEA_URL"]
    gitea_username = gitea_config["GITEA_USERNAME"]
    gitea_token = gitea_config["GITEA_TOKEN"]
    
    # Create Gitea repository
    data = json.dumps({
        "name": repo_name,
        "description": f"{repo_name} project",
        "private": False,
        "auto_init": False
    }).encode()
    
    req = urllib.request.Request(
        f"{gitea_url}/api/v1/user/repos",
        data=data,
        headers={
            "Authorization": f"token {gitea_token}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            response.read()
        print(f"Created Gitea repository: {gitea_url}/{gitea_username}/{repo_name}")
    except Exception as e:
        print(f"Warning: Could not create Gitea repository: {e}")
        print("You may need to create it manually.")
        return
    
    # Add remote
    run_command(
        ["git", "remote", "add", "origin", f"{gitea_url}/{gitea_username}/{repo_name}.git"],
        cwd=project_path
    )
    
    # Create develop branch
    run_command(["git", "checkout", "-b", "develop"], cwd=project_path)
    
    # Initial commit
    run_command(["git", "add", "."], cwd=project_path)
    run_command(["git", "commit", "-m", "chore: initial project setup"], cwd=project_path)
    
    # Push branches
    try:
        run_command(["git", "push", "-u", "origin", "develop"], cwd=project_path)
        run_command(["git", "checkout", "main"], cwd=project_path)
        run_command(["git", "merge", "develop"], cwd=project_path)
        run_command(["git", "push", "-u", "origin", "main"], cwd=project_path)
        run_command(["git", "checkout", "develop"], cwd=project_path)
        print("Pushed to Gitea successfully")
    except Exception:
        print("Note: Could not push to Gitea. You may need to push manually.")


def main() -> NoReturn:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Initialize a new Python project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--path", default=".", help="Path where to create the project")
    parser.add_argument("--no-git", action="store_true", help="Skip git initialization")
    
    args = parser.parse_args()
    
    project_name = args.project_name
    package_name = project_name.replace("-", "_")
    base_path = Path(args.path).resolve()
    project_path = base_path / project_name
    
    if project_path.exists():
        print(f"Error: Directory {project_path} already exists")
        sys.exit(1)
    
    print(f"Creating project: {project_name}")
    print(f"Location: {project_path}")
    print()
    
    # Create structure
    create_project_structure(project_path, package_name)
    print("Created project structure")
    
    # Create configuration files
    create_gitignore(project_path)
    create_pyproject_toml(project_path, project_name, package_name)
    create_main_file(project_path, package_name)
    create_example_test(project_path, package_name)
    create_planning_file(project_path)
    print("Created configuration files")
    
    # Initialize uv
    print("Initializing uv environment...")
    run_command(["uv", "sync", "--dev"], cwd=project_path)
    print("Installed dependencies")
    
    # Initialize git
    if not args.no_git:
        print("Initializing git repository...")
        initialize_git(project_path, project_name)
    
    print()
    print(f"Project {project_name} created successfully!")
    print()
    print("Next steps:")
    print(f"  cd {project_name}")
    print("  uv run pytest  # Run tests")
    print("  uv run ruff format .  # Format code")
    print("  uv run mypy src/  # Type check")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
