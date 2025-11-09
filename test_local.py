"""
Local testing script for the GitHub Repository Analyzer
Run this to test the core functionality without deploying
"""
import os
from dotenv import load_dotenv
from src.documentation_generator.github_client import GitHubClient
from src.documentation_generator.processor import CodebaseProcessor
from src.documentation_generator.claude_client import ClaudeClient

# Load environment variables
load_dotenv()

def test_analyze(repo_url: str, prompt: str):
    """Test the analysis pipeline locally"""
    print(f"Testing analysis for: {repo_url}")
    print(f"Prompt: {prompt}\n")

    try:
        # Get API keys from environment
        github_token = os.getenv('GITHUB_TOKEN')
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        # Initialize clients
        print("Initializing clients...")
        github_client = GitHubClient(github_token=github_token)
        processor = CodebaseProcessor()
        claude_client = ClaudeClient(api_key=anthropic_api_key)

        # Fetch repository data
        print("Fetching repository data...")
        repo_data = github_client.fetch_repository(repo_url)
        print(f"✓ Fetched repository: {repo_data.get('full_name')}")

        # Build context summary
        print("Building context summary...")
        context_summary = processor.build_context_summary(repo_data)
        print(f"✓ Built context summary ({len(context_summary)} characters)")

        # Get codebase stats
        stats = processor.calculate_codebase_stats(repo_data)
        print(f"✓ Calculated stats: {stats['total_files']} files, {stats.get('total_lines', 0)} lines")

        # Analyze with Claude
        print("\nAnalyzing with Claude AI...")
        analysis = claude_client.analyze_codebase(
            codebase_context=context_summary,
            user_prompt=prompt
        )

        # Print results
        print("\n" + "="*80)
        print("ANALYSIS RESULT")
        print("="*80)
        print(analysis)
        print("="*80)

        # Print metadata
        print("\nMETADATA:")
        print(f"  Repository: {repo_data.get('full_name')}")
        print(f"  Language: {repo_data.get('language')}")
        print(f"  Stars: {repo_data.get('stars')}")
        print(f"  Total Files: {stats['total_files']}")
        print(f"  Total Lines: {stats.get('total_lines', 'N/A')}")

        return {
            "success": True,
            "analysis": analysis,
            "stats": stats,
            "metadata": {
                "language": repo_data.get('language'),
                "stars": repo_data.get('stars'),
                "description": repo_data.get('description'),
            }
        }

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Example test cases
    print("GitHub Repository Analyzer - Local Testing\n")

    # Test 1: Small repository
    result = test_analyze(
        repo_url="https://github.com/anthropics/anthropic-sdk-python",
        prompt="Provide a brief overview of this repository, including its main purpose and key features."
    )

    # Uncomment to test additional repositories
    # result = test_analyze(
    #     repo_url="https://github.com/vercel/next.js",
    #     prompt="What are the main components of this framework?"
    # )
