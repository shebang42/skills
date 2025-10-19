#!/usr/bin/env python3
"""Git and Gitea configuration loader.

Reads configuration from environment variables for security and portability.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GiteaConfig:
    """Gitea server configuration."""
    
    url: str
    username: str
    token: str
    
    @classmethod
    def from_env(cls) -> Optional["GiteaConfig"]:
        """Load configuration from environment variables.
        
        Required environment variables:
        - GITEA_URL: Gitea server URL (e.g., https://[your-gitea-server]:3000)
        - GITEA_USERNAME: Your Gitea username
        - GITEA_TOKEN: Your Gitea API access token
        
        Returns:
            GiteaConfig if all variables are set, None otherwise
        """
        url = os.getenv("GITEA_URL")
        username = os.getenv("GITEA_USERNAME")
        token = os.getenv("GITEA_TOKEN")
        
        if not all([url, username, token]):
            return None
        
        return cls(url=url, username=username, token=token)
    
    def get_repo_url(self, repo_name: str) -> str:
        """Get the full repository URL."""
        return f"{self.url}/{self.username}/{repo_name}.git"
    
    def get_api_url(self) -> str:
        """Get the API base URL."""
        return f"{self.url}/api/v1"


def load_config() -> GiteaConfig:
    """Load Gitea configuration from environment.
    
    Raises:
        RuntimeError: If required environment variables are not set
    """
    config = GiteaConfig.from_env()
    
    if config is None:
        raise RuntimeError(
            "Gitea configuration not found. Please set environment variables:\n"
            "  GITEA_URL=https://[your-gitea-server]:3000\n"
            "  GITEA_USERNAME=your-username\n"
            "  GITEA_TOKEN=your-access-token"
        )
    
    return config


if __name__ == "__main__":
    """Test configuration loading."""
    try:
        config = load_config()
        print(f"Gitea URL: {config.url}")
        print(f"Username: {config.username}")
        print(f"Token: {'*' * len(config.token)}")  # Don't print actual token
        print(f"API URL: {config.get_api_url()}")
    except RuntimeError as e:
        print(f"Error: {e}")
