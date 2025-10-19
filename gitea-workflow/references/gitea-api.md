# Gitea API Reference

Common Gitea API operations using environment variables for authentication.

## Configuration

All examples use environment variables:

```python
import os

GITEA_URL = os.getenv("GITEA_URL")
GITEA_USERNAME = os.getenv("GITEA_USERNAME")
GITEA_TOKEN = os.getenv("GITEA_TOKEN")

headers = {
    "Authorization": f"token {GITEA_TOKEN}",
    "Content-Type": "application/json"
}
```

## Create Repository

```python
import json
import urllib.request

data = json.dumps({
    "name": "my-project",
    "description": "Project description",
    "private": False,
    "auto_init": False
}).encode()

req = urllib.request.Request(
    f"{GITEA_URL}/api/v1/user/repos",
    data=data,
    headers=headers
)

with urllib.request.urlopen(req) as response:
    repo_data = json.loads(response.read())
    print(f"Created: {repo_data['html_url']}")
```

## List Repositories

```python
req = urllib.request.Request(
    f"{GITEA_URL}/api/v1/user/repos",
    headers=headers
)

with urllib.request.urlopen(req) as response:
    repos = json.loads(response.read())
    for repo in repos:
        print(f"{repo['name']}: {repo['html_url']}")
```

## Get Repository Info

```python
req = urllib.request.Request(
    f"{GITEA_URL}/api/v1/repos/{GITEA_USERNAME}/my-project",
    headers=headers
)

with urllib.request.urlopen(req) as response:
    repo = json.loads(response.read())
    print(f"Name: {repo['name']}")
    print(f"Description: {repo['description']}")
    print(f"Stars: {repo['stars_count']}")
```

## Create Pull Request

```python
data = json.dumps({
    "title": "Add new feature",
    "body": "This PR adds...",
    "head": "feature/new-feature",
    "base": "develop"
}).encode()

req = urllib.request.Request(
    f"{GITEA_URL}/api/v1/repos/{GITEA_USERNAME}/my-project/pulls",
    data=data,
    headers=headers
)

with urllib.request.urlopen(req) as response:
    pr = json.loads(response.read())
    print(f"PR created: {pr['html_url']}")
```

## List Pull Requests

```python
req = urllib.request.Request(
    f"{GITEA_URL}/api/v1/repos/{GITEA_USERNAME}/my-project/pulls",
    headers=headers
)

with urllib.request.urlopen(req) as response:
    prs = json.loads(response.read())
    for pr in prs:
        print(f"#{pr['number']}: {pr['title']} ({pr['state']})")
```

## API Endpoints

Base URL: `{GITEA_URL}/api/v1`

### Repositories
- `POST /user/repos` - Create repository
- `GET /user/repos` - List user repositories
- `GET /repos/{owner}/{repo}` - Get repository
- `DELETE /repos/{owner}/{repo}` - Delete repository

### Pull Requests
- `GET /repos/{owner}/{repo}/pulls` - List PRs
- `POST /repos/{owner}/{repo}/pulls` - Create PR
- `GET /repos/{owner}/{repo}/pulls/{index}` - Get PR
- `PATCH /repos/{owner}/{repo}/pulls/{index}` - Update PR

### Branches
- `GET /repos/{owner}/{repo}/branches` - List branches
- `POST /repos/{owner}/{repo}/branches` - Create branch
- `DELETE /repos/{owner}/{repo}/branches/{branch}` - Delete branch

## Error Handling

```python
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
except urllib.error.HTTPError as e:
    if e.code == 409:
        print("Resource already exists")
    elif e.code == 404:
        print("Resource not found")
    else:
        print(f"Error: {e.code} - {e.read()}")
```

## Complete Example

```python
#!/usr/bin/env python3
"""Example: Create repo and PR workflow."""

import json
import os
import urllib.request


def get_headers() -> dict:
    """Get API headers with auth token."""
    token = os.getenv("GITEA_TOKEN")
    if not token:
        raise RuntimeError("GITEA_TOKEN not set")
    
    return {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }


def create_repo(name: str) -> dict:
    """Create a new repository."""
    url = os.getenv("GITEA_URL")
    data = json.dumps({
        "name": name,
        "auto_init": True
    }).encode()
    
    req = urllib.request.Request(
        f"{url}/api/v1/user/repos",
        data=data,
        headers=get_headers()
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


if __name__ == "__main__":
    repo = create_repo("test-repo")
    print(f"Created: {repo['html_url']}")
```
