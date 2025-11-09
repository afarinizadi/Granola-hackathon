"""
GitHub Repository Fetcher
Handles fetching repository contents via GitHub API
"""
import os
from typing import Dict, List, Optional
from github import Github, GithubException
import requests


class GitHubClient:
    """Client for fetching GitHub repository contents"""

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub client

        Args:
            github_token: Optional GitHub personal access token for higher rate limits
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')

        # Filter out placeholder tokens
        if self.github_token and (
            'your_' in self.github_token.lower() or
            'placeholder' in self.github_token.lower() or
            len(self.github_token) < 20
        ):
            print("Warning: Invalid GitHub token detected, proceeding without authentication")
            self.github_token = None

        self.github = Github(self.github_token) if self.github_token else Github()

    def parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """
        Parse GitHub repository URL to extract owner and repo name

        Args:
            repo_url: GitHub repository URL (e.g., https://github.com/user/repo)

        Returns:
            Tuple of (owner, repo_name)

        Raises:
            ValueError: If URL is not a valid GitHub repository URL
        """
        # Remove trailing slashes and .git extension
        repo_url = repo_url.rstrip('/').rstrip('.git')

        # Handle different URL formats
        if 'github.com/' in repo_url:
            parts = repo_url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return parts[0], parts[1]

        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

    def fetch_repository(self, repo_url: str) -> Dict:
        """
        Fetch repository metadata and contents

        Args:
            repo_url: GitHub repository URL

        Returns:
            Dictionary containing repository information
        """
        owner, repo_name = self.parse_repo_url(repo_url)

        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")

            # Get repository metadata
            repo_data = {
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'default_branch': repo.default_branch,
                'size': repo.size,
                'topics': repo.get_topics(),
                'license': repo.license.name if repo.license else None,
            }

            # Fetch file tree
            repo_data['file_tree'] = self._build_file_tree(repo)

            # Fetch important files content
            repo_data['files'] = self._fetch_files(repo)

            return repo_data

        except GithubException as e:
            raise Exception(f"Failed to fetch repository: {str(e)}")

    def _build_file_tree(self, repo) -> Dict:
        """
        Build a hierarchical file tree of the repository (simplified for rate limits)

        Args:
            repo: PyGithub repository object

        Returns:
            Dictionary representing the file tree structure
        """
        try:
            # Only fetch root level to reduce API calls
            contents = repo.get_contents("")
            tree = {'dirs': {}, 'files': []}

            for content in contents:
                if content.type == "dir":
                    tree['dirs'][content.name] = {
                        'path': content.path,
                        'note': 'Directory listing limited to save API calls'
                    }
                else:
                    tree['files'].append({
                        'name': content.name,
                        'path': content.path,
                        'size': content.size
                    })

            return tree

        except GithubException as e:
            return {'error': str(e), 'dirs': {}, 'files': []}

    def _fetch_files(self, repo, max_file_size: int = 100000) -> List[Dict]:
        """
        Fetch content of important files from the repository

        Args:
            repo: PyGithub repository object
            max_file_size: Maximum file size to fetch (in bytes)

        Returns:
            List of dictionaries containing file information and content
        """
        files_to_fetch = [
            'README.md', 'README.rst', 'README.txt',
            'package.json', 'requirements.txt', 'setup.py', 'pyproject.toml',
            'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle',
            '.gitignore', 'LICENSE', 'Makefile', 'Dockerfile'
        ]

        fetched_files = []

        for filename in files_to_fetch:
            try:
                file_content = repo.get_contents(filename)
                if file_content.size <= max_file_size:
                    try:
                        content = file_content.decoded_content.decode('utf-8')
                        fetched_files.append({
                            'name': filename,
                            'path': file_content.path,
                            'size': file_content.size,
                            'content': content
                        })
                    except UnicodeDecodeError:
                        # Skip binary files
                        pass
            except GithubException:
                # File doesn't exist, skip
                continue

        return fetched_files

    def get_repository_languages(self, repo_url: str) -> Dict[str, int]:
        """
        Get programming languages used in the repository

        Args:
            repo_url: GitHub repository URL

        Returns:
            Dictionary of languages and their byte counts
        """
        owner, repo_name = self.parse_repo_url(repo_url)

        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            return repo.get_languages()
        except GithubException as e:
            raise Exception(f"Failed to fetch languages: {str(e)}")
