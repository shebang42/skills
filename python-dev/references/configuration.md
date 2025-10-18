# Configuration Setup

## Gitea Credentials

The Python development skill requires Gitea credentials for automatic repository creation. These credentials are **never stored in the skill itself** for security reasons.

### Setup Methods

#### Method 1: Configuration File (Recommended)

Create a configuration file at `~/.config/python-dev/config`:

```bash
# Create config directory
mkdir -p ~/.config/python-dev

# Create config file
cat > ~/.config/python-dev/config << 'EOF'
# Gitea Configuration
GITEA_URL=https://git.home:3443 
GITEA_USERNAME=your-username
GITEA_TOKEN=your-access-token
EOF

# Secure the file (readable only by you)
chmod 600 ~/.config/python-dev/config
```

**Benefits:**
- Persistent across sessions
- Separate from environment
- Easy to update
- Secure file permissions

#### Method 2: Environment Variables

Export environment variables in your shell:

```bash
# Add to ~/.bashrc or ~/.zshrc
export GITEA_URL="https://git.home:3443"
export GITEA_USERNAME="your-username"
export GITEA_TOKEN="your-access-token"
```

Then reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

**Benefits:**
- Works with existing environment variable workflows
- Can be set per-session if needed

### Configuration Priority

The skill checks credentials in this order:

1. **Config file** (`~/.config/python-dev/config`) - checked first
2. **Environment variables** - checked if config file not found or incomplete
3. **No credentials** - script continues without Gitea integration

If no credentials are found, the `init_project.py` script will:
- Print a warning with setup instructions
- Create the local git repository
- Skip remote repository creation
- Allow manual setup later

### Obtaining a Gitea Access Token

1. Log in to your Gitea instance (https://git.home:3443)
2. Navigate to Settings → Applications
3. Generate a new token with these permissions:
   - `write:repository` - Create and manage repositories
   - `write:organization` - Manage organization repositories (if needed)
4. Copy the token immediately (it's only shown once)
5. Add it to your configuration

### Security Best Practices

1. **Never commit credentials** to version control
2. **Use restrictive file permissions** (600 for config file)
3. **Rotate tokens regularly** for better security
4. **Use separate tokens** for different purposes
5. **Revoke unused tokens** in Gitea settings

### Verifying Configuration

Test your configuration:

```bash
# Check if config file exists and is readable
cat ~/.config/python-dev/config

# Test Gitea API access
curl -H "Authorization: token ${GITEA_TOKEN}" \
  ${GITEA_URL}/api/v1/user
```

### Troubleshooting

**Error: "Gitea configuration not found"**
- Ensure config file exists at `~/.config/python-dev/config`
- Or set environment variables: `GITEA_URL`, `GITEA_USERNAME`, `GITEA_TOKEN`

**Error: "Could not create Gitea repository"**
- Verify token has correct permissions
- Check if repository name already exists
- Confirm Gitea server is accessible
- Test with curl command above

**Error: "Could not push to Gitea"**
- Verify git is configured with your email/name
- Check network connectivity to Gitea server
- Ensure you have push permissions

### Manual Repository Setup

If automatic setup fails, create repository manually:

```bash
# 1. Create repository via Gitea web UI

# 2. Add remote to existing local repository
cd your-project
git remote add origin ${GITEA_URL}/${GITEA_USERNAME}/your-project.git

# 3. Push branches
git push -u origin develop
git checkout main
git push -u origin main
git checkout develop
```

## Configuration Template

A template configuration file is available in `assets/config.template`:

```bash
# Copy template
cp assets/config.template ~/.config/python-dev/config

# Edit with your credentials
nano ~/.config/python-dev/config

# Secure the file
chmod 600 ~/.config/python-dev/config
```
