"""
Documentation Generator Package

This package contains the core components for analyzing GitHub repositories
and generating comprehensive documentation using Claude AI.
"""

from .github_client import GitHubClient
from .processor import CodebaseProcessor
from .claude_client import ClaudeClient

__all__ = ['GitHubClient', 'CodebaseProcessor', 'ClaudeClient']
