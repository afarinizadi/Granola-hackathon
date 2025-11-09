"""
Claude API Integration
Handles interactions with the Claude API for codebase analysis
"""
import os
from typing import Optional
from anthropic import Anthropic, APIError


class ClaudeClient:
    """Client for interacting with Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude API client

        Args:
            api_key: Optional Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Claude model
        self.max_tokens = 4096

    def analyze_codebase(
        self,
        codebase_context: str,
        user_prompt: str,
        temperature: float = 1.0
    ) -> str:
        """
        Analyze a codebase using Claude API

        Args:
            codebase_context: Formatted context about the codebase
            user_prompt: User's analysis prompt/question
            temperature: Temperature for response generation (0.0-1.0)

        Returns:
            Claude's analysis response as a string

        Raises:
            Exception: If API call fails
        """
        try:
            # Construct the system prompt
            system_prompt = """You are an expert software engineer and code analyst.
You will be provided with information about a GitHub repository including its structure,
dependencies, key files, and metadata. Your task is to analyze this codebase and provide
insightful, accurate, and comprehensive responses to the user's questions or requests.

Focus on:
- Understanding the overall architecture and design patterns
- Identifying key technologies and frameworks used
- Explaining how different components interact
- Highlighting notable features or implementation details
- Providing practical insights for developers working with this code

Be thorough but concise. Use your expertise to provide value beyond what's immediately
obvious from the file structure."""

            # Construct the user message
            user_message = f"""Here is the repository information:

{codebase_context}

---

User's Request:
{user_prompt}

Please analyze the codebase and respond to the user's request."""

            # Make the API call
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            # Extract and return the response text
            if message.content and len(message.content) > 0:
                return message.content[0].text
            else:
                return "No response generated"

        except APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to analyze codebase: {str(e)}")

    def analyze_with_streaming(
        self,
        codebase_context: str,
        user_prompt: str,
        temperature: float = 1.0
    ):
        """
        Analyze a codebase using Claude API with streaming response

        Args:
            codebase_context: Formatted context about the codebase
            user_prompt: User's analysis prompt/question
            temperature: Temperature for response generation (0.0-1.0)

        Yields:
            Text chunks as they are received from the API

        Raises:
            Exception: If API call fails
        """
        try:
            system_prompt = """You are an expert software engineer and code analyst.
You will be provided with information about a GitHub repository including its structure,
dependencies, key files, and metadata. Your task is to analyze this codebase and provide
insightful, accurate, and comprehensive responses to the user's questions or requests.

Focus on:
- Understanding the overall architecture and design patterns
- Identifying key technologies and frameworks used
- Explaining how different components interact
- Highlighting notable features or implementation details
- Providing practical insights for developers working with this code

Be thorough but concise. Use your expertise to provide value beyond what's immediately
obvious from the file structure."""

            user_message = f"""Here is the repository information:

{codebase_context}

---

User's Request:
{user_prompt}

Please analyze the codebase and respond to the user's request."""

            # Make streaming API call
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to analyze codebase: {str(e)}")

    def set_model(self, model: str):
        """
        Set the Claude model to use

        Args:
            model: Model identifier (e.g., 'claude-sonnet-4-20250514')
        """
        self.model = model

    def set_max_tokens(self, max_tokens: int):
        """
        Set the maximum tokens for responses

        Args:
            max_tokens: Maximum number of tokens to generate
        """
        self.max_tokens = max_tokens
