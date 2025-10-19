#!/usr/bin/env python3
"""Initialize a new Python project with standard structure."""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a shell command."""
    try:
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        sys.exit(1)


def create_structure(project_path: Path, package_name: str) -> None:
    """Create project directory structure."""
    # Main directories
    (project_path / "src" / package_name).mkdir(parents=True)
    (project_path / "tests").mkdir()
    
    # Package subdirectories
    for subdir in ["models", "services", "repositories", "utils"]:
        (project_path / "src" / package_name / subdir).mkdir()
        (project_path / "src" / package_name / subdir / "__init__.py").touch()
    
    # Test subdirectories
    for subdir in ["test_models", "test_services", "integration"]:
        (project_path / "tests" / subdir).mkdir()
        (project_path / "tests" / subdir / "__init__.py").touch()
    
    # Init files
    (project_path / "src" / package_name / "__init__.py").touch()
    (project_path / "tests" / "__init__.py").touch()


def create_pyproject_toml(project_path: Path, project_name: str) -> None:
    """Create pyproject.toml."""
    content = f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.13"
dependencies = ["pydantic>=2.9.0"]

[project.optional-dependencies]
dev = ["pytest>=8.3.0", "pytest-cov>=5.0.0", "mypy>=1.11.0", "ruff>=0.6.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--cov=src", "--cov-report=html", "--cov-report=term-missing"]

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 80

[tool.mypy]
python_version = "3.13"
strict = true

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
ignore = ["E501", "B008"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/**/*" = ["ARG"]
'''
    (project_path / "pyproject.toml").write_text(content)


def create_gitignore(project_path: Path) -> None:
    """Create .gitignore."""
    content = """__pycache__/
*.py[cod]
.Python
.venv/
dist/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.env
"""
    (project_path / ".gitignore").write_text(content)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Initialize Python project")
    parser.add_argument("project_name", help="Project name")
    parser.add_argument("--path", default=".", help="Parent directory")
    args = parser.parse_args()
    
    project_name = args.project_name
    package_name = project_name.replace("-", "_")
    project_path = Path(args.path).resolve() / project_name
    
    if project_path.exists():
        print(f"Error: {project_path} already exists")
        sys.exit(1)
    
    print(f"Creating project: {project_name}")
    
    create_structure(project_path, package_name)
    create_pyproject_toml(project_path, project_name)
    create_gitignore(project_path)
    
    # Create main.py
    (project_path / "src" / package_name / "main.py").write_text(
        f'def main() -> None:\n    print("Hello from {package_name}!")\n'
    )
    
    # Create example test
    (project_path / "tests" / "test_example.py").write_text(
        'def test_example() -> None:\n    assert True\n'
    )
    
    # Initialize uv
    print("Installing dependencies...")
    run_command(["uv", "sync", "--dev"], cwd=project_path)
    
    print(f"\nProject created at: {project_path}")
    print("\nNext steps:")
    print(f"  cd {project_name}")
    print("  uv run pytest")


if __name__ == "__main__":
    main()
