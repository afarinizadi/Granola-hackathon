"""
Vercel Serverless Function: Repository Analyzer
Endpoint: POST /api/analyze
"""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler

# Add src directory to Python path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.documentation_generator.github_client import GitHubClient
from src.documentation_generator.processor import CodebaseProcessor
from src.documentation_generator.claude_client import ClaudeClient


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""

    def do_POST(self):
        """Handle POST requests to /api/analyze"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')

            # Parse JSON request
            try:
                request_data = json.loads(body)
            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON in request body")
                return

            # Validate required fields
            repo_url = request_data.get('repo_url')
            user_prompt = request_data.get('prompt')

            if not repo_url:
                self._send_error(400, "Missing required field: repo_url")
                return

            if not user_prompt:
                self._send_error(400, "Missing required field: prompt")
                return

            # Validate GitHub URL format
            if not self._is_valid_github_url(repo_url):
                self._send_error(400, "Invalid GitHub repository URL")
                return

            # Optional parameters
            github_token = request_data.get('github_token') or os.getenv('GITHUB_TOKEN')
            anthropic_api_key = request_data.get('anthropic_api_key') or os.getenv('ANTHROPIC_API_KEY')

            if not anthropic_api_key:
                self._send_error(500, "ANTHROPIC_API_KEY is not configured")
                return

            # Process the repository
            try:
                # Initialize clients
                github_client = GitHubClient(github_token=github_token)
                processor = CodebaseProcessor()
                claude_client = ClaudeClient(api_key=anthropic_api_key)

                # Fetch repository data
                repo_data = github_client.fetch_repository(repo_url)

                # Build context summary
                context_summary = processor.build_context_summary(repo_data)

                # Get codebase stats
                stats = processor.calculate_codebase_stats(repo_data)

                # Analyze with Claude
                analysis = claude_client.analyze_codebase(
                    codebase_context=context_summary,
                    user_prompt=user_prompt
                )

                # Prepare response
                response_data = {
                    "success": True,
                    "repo_url": repo_url,
                    "repo_name": repo_data.get('full_name'),
                    "summary": analysis,
                    "stats": stats,
                    "metadata": {
                        "language": repo_data.get('language'),
                        "stars": repo_data.get('stars'),
                        "description": repo_data.get('description'),
                    }
                }

                self._send_success(response_data)

            except ValueError as e:
                self._send_error(400, str(e))
            except Exception as e:
                self._send_error(500, f"Failed to process repository: {str(e)}")

        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")

    def do_GET(self):
        """Handle GET requests - return API info"""
        info = {
            "service": "GitHub Repository Analyzer",
            "version": "1.0.0",
            "endpoint": "/api/analyze",
            "method": "POST",
            "description": "Analyzes GitHub repositories using Claude AI",
            "required_fields": ["repo_url", "prompt"],
            "optional_fields": ["github_token", "anthropic_api_key"],
            "example": {
                "repo_url": "https://github.com/user/repo",
                "prompt": "Analyze this codebase and provide a comprehensive summary"
            }
        }
        self._send_success(info)

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self._send_cors_headers()
        self.send_response(200)
        self.end_headers()

    def _send_success(self, data: dict):
        """Send successful JSON response"""
        self._send_cors_headers()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def _send_error(self, status_code: int, message: str):
        """Send error JSON response"""
        self._send_cors_headers()
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        error_response = {
            "success": False,
            "error": message,
            "status_code": status_code
        }
        self.wfile.write(json.dumps(error_response, indent=2).encode('utf-8'))

    def _send_cors_headers(self):
        """Send CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _is_valid_github_url(self, url: str) -> bool:
        """
        Validate if the URL is a valid GitHub repository URL

        Args:
            url: URL to validate

        Returns:
            True if valid GitHub URL, False otherwise
        """
        if not url:
            return False

        # Check if URL contains github.com
        if 'github.com' not in url.lower():
            return False

        # Check if URL has the expected format
        try:
            parts = url.rstrip('/').rstrip('.git').split('github.com/')[-1].split('/')
            # Should have at least owner and repo name
            return len(parts) >= 2 and all(parts[:2])
        except:
            return False
