# Environment Setup Guide

Quick guide to set up environment variables for Gitea integration.

## Why Environment Variables?

**Security & Portability**: Credentials are stored outside your code and version control, making your skills:
- ✅ Portable across different environments
- ✅ Secure (no secrets in Git)
- ✅ Multi-user friendly (each user uses their own credentials)
- ✅ Easy to update without code changes

## Setup Options

### Option 1: Shell Profile (Recommended for Permanent Setup)

Add to your shell profile for automatic loading:

**For Bash** (`~/.bashrc`):
```bash
# Add these lines to ~/.bashrc
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-gitea-access-token]"

# Reload shell
source ~/.bashrc
```

**For Zsh** (`~/.zshrc`):
```bash
# Add these lines to ~/.zshrc
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-gitea-access-token]"

# Reload shell
source ~/.zshrc
```

### Option 2: direnv (Recommended for Project-Specific)

`direnv` automatically loads environment variables when you enter a directory.

**Install direnv**:
```bash
# Ubuntu/Debian
sudo apt install direnv

# macOS
brew install direnv

# Add hook to your shell
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc  # For Bash
source ~/.bashrc
```

**Create `.envrc` in your workspace**:
```bash
cd ~/workspace

cat > .envrc << 'ENVRC'
# Gitea Configuration
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-gitea-access-token]"
ENVRC

# Allow directory
direnv allow .
```

### Option 3: Manual Export (Temporary)

```bash
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-gitea-access-token]"
```

## Verify Setup

```bash
# Check if variables are set
echo $GITEA_URL
echo $GITEA_USERNAME

# Test configuration
python3 << 'PYEOF'
import os
url = os.getenv("GITEA_URL")
username = os.getenv("GITEA_USERNAME")
token = os.getenv("GITEA_TOKEN")

if all([url, username, token]):
    print("✅ Configuration successful!")
    print(f"   URL: {url}")
    print(f"   Username: {username}")
else:
    print("❌ Configuration incomplete")
PYEOF
```

## Getting Your Gitea Access Token

1. Log in to Gitea (https://your-gitea-server:3000)
2. Settings → Applications
3. Generate new token
4. Copy and use in configuration

## Recommended: Use direnv

Create `.envrc` in your workspace with your credentials, and add it to `.gitignore`:

```bash
# .envrc (in .gitignore)
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-gitea-access-token]"
```

Create `.envrc.example` template for other users:

```bash
# .envrc.example (commit this)
export GITEA_URL="https://your-gitea-server:3000"
export GITEA_USERNAME="[your-username]"
export GITEA_TOKEN="[your-gitea-access-token]"
```

This keeps secrets out of version control while providing documentation for setup.
