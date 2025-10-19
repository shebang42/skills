#!/usr/bin/env python3
"""Initialize Git repository and create on Gitea.

Reads Gitea configuration from environment variables for security.
"""

import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

from gitea_config import load_config


def run_git(cmd: list[str], cwd: Path) -> None:
    """Run git command."""
    try:
        subprocess.run(
            ["git"] + cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}")
        sys.exit(1)


def create_gitea_repo(repo_name: str, description: str = "") -> None:
    """Create repository on Gitea using API."""
    config = load_config()
    
    data = json.dumps({
        "name": repo_name,
        "description": description or f"{repo_name} project",
        "private": False,
        "auto_init": False
    }).encode()
    
    req = urllib.request.Request(
        f"{config.get_api_url()}/user/repos",
        data=data,
        headers={
            "Authorization": f"token {config.token}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            response.read()
        print(f"Created Gitea repository: {config.url}/{config.username}/{repo_name}")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"Repository {repo_name} already exists on Gitea")
        else:
            print(f"Failed to create repository: {e}")
            sys.exit(1)


def init_git_repo(project_path: Path, repo_name: str) -> None:
    """Initialize Git repository with gitflow structure."""
    config = load_config()
    
    print(f"Initializing Git repository in {project_path}")
    
    # Initialize repo
    run_git(["init"], project_path)
    run_git(["branch", "-M", "main"], project_path)
    
    # Add remote
    remote_url = config.get_repo_url(repo_name)
    run_git(["remote", "add", "origin", remote_url], project_path)
    
    # Create develop branch
    run_git(["checkout", "-b", "develop"], project_path)
    
    # Initial commit
    run_git(["add", "."], project_path)
    run_git(["commit", "-m", "chore: initial project setup"], project_path)
    
    print("Pushing to Gitea...")
    try:
        # Push develop
        run_git(["push", "-u", "origin", "develop"], project_path)
        
        # Push main
        run_git(["checkout", "main"], project_path)
        run_git(["merge", "develop"], project_path)
        run_git(["push", "-u", "origin", "main"], project_path)
        
        # Back to develop
        run_git(["checkout", "develop"], project_path)
        
        print("Successfully pushed to Gitea")
    except Exception as e:
        print(f"Warning: Could not push to Gitea: {e}")
        print("You may need to push manually")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize Git repo and create on Gitea"
    )
    parser.add_argument("repo_name", help="Repository name")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument(
        "--description",
        default="",
        help="Repository description"
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Don't push to Gitea"
    )
    
    args = parser.parse_args()
    
    project_path = Path(args.path).resolve()
    
    if not project_path.exists():
        print(f"Error: Path {project_path} does not exist")
        sys.exit(1)
    
    # Create Gitea repository
    print("Creating Gitea repository...")
    create_gitea_repo(args.repo_name, args.description)
    
    # Initialize Git
    init_git_repo(project_path, args.repo_name)
    
    print("\nRepository initialized successfully!")
    print(f"Branches: main, develop")
    print(f"Current branch: develop")


if __name__ == "__main__":
    main()
