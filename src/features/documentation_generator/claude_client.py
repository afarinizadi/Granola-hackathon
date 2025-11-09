"""
Claude API Integration via AWS Bedrock
Handles interactions with Claude via AWS Bedrock for codebase analysis
"""
import os
import json
from typing import Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class ClaudeClient:
    """Client for interacting with Claude via AWS Bedrock"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client for AWS Bedrock

        Args:
            api_key: Optional (kept for compatibility, uses AWS credentials instead)
        """
        # Get AWS region from environment variable, default to us-east-1
        aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        
        # Use AWS credentials from environment or AWS profile
        self.client = boto3.client('bedrock-runtime', region_name=aws_region)
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude 3 Sonnet on Bedrock
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

            # Make the API call to Bedrock
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "temperature": temperature,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }

            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )

            # Parse the response
            response_body = json.loads(response['body'].read())
            
            # Extract and return the response text
            if response_body.get('content') and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                return "No response generated"

        except (ClientError, BotoCoreError) as e:
            raise Exception(f"AWS Bedrock error: {str(e)}")
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

            # Note: Streaming not supported in this simplified AWS Bedrock implementation
            # Fall back to regular API call
            return self.analyze_codebase(codebase_context, user_prompt, temperature)

        except (ClientError, BotoCoreError) as e:
            raise Exception(f"AWS Bedrock error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to analyze codebase: {str(e)}")

    def set_model(self, model_id: str):
        """
        Set the Claude model to use on Bedrock

        Args:
            model_id: Bedrock model identifier (e.g., 'anthropic.claude-3-sonnet-20240229-v1:0')
        """
        self.model_id = model_id

    def set_max_tokens(self, max_tokens: int):
        """
        Set the maximum tokens for responses

        Args:
            max_tokens: Maximum number of tokens to generate
        """
        self.max_tokens = max_tokens
