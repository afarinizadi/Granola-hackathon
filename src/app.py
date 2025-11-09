"""
Main application that combines documentation generation with video creation.
This script:
1. Analyzes a GitHub repository and generates documentation
2. Uses the generated documentation to create a video with HeyGen
"""
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features.documentation_generator.github_client import GitHubClient
from src.features.documentation_generator.processor import CodebaseProcessor
from src.features.documentation_generator.claude_client import ClaudeClient
from src.features.text_to_video.hey_gen_generator import create_video, check_video_status

# Load environment variables
load_dotenv()

# Configuration
HEYGEN_API_KEY = "sk_V2_hgu_kfBHVYRDOpI_iyjgSDFNyw4p9GcD63krhShUd8UjGwWj"
AVATAR_ID = "Annie_Office_Sitting_Side_2_public"


def generate_documentation(repo_url: str, prompt: str):
    """Generate documentation using the documentation generator"""
    print(f"Analyzing repository: {repo_url}")
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

        print("Documentation generation completed!")
        
        return {
            "success": True,
            "analysis": analysis,
            "stats": stats,
            "metadata": {
                "repo_name": repo_data.get('full_name'),
                "language": repo_data.get('language'),
                "stars": repo_data.get('stars'),
                "description": repo_data.get('description'),
            }
        }

    except Exception as e:
        print(f"\nError in documentation generation: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def create_video_from_documentation(documentation_result):
    """Create a video using HeyGen from the documentation analysis"""
    if not documentation_result["success"]:
        print("Cannot create video: Documentation generation failed")
        return None

    # Extract the analysis text
    analysis_text = documentation_result["analysis"]
    
    # Truncate if too long (HeyGen has limits)
    max_length = 2000  # Adjust based on HeyGen's limits
    if len(analysis_text) > max_length:
        analysis_text = analysis_text[:max_length] + "..."
        print(f"Text truncated to {max_length} characters for video generation")

    print(f"\nCreating video from documentation...")
    print(f"Text length: {len(analysis_text)} characters")
    
    # Create video using HeyGen
    video_id = create_video(analysis_text, AVATAR_ID)
    
    if video_id:
        print(f"Video creation initiated with ID: {video_id}")
        # Check video status
        check_video_status(video_id)
        return video_id
    else:
        print("Failed to create video")
        return None


def main():
    """Main application flow"""
    print("="*80)
    print("GRANOLA HACKATHON - DOCUMENTATION TO VIDEO GENERATOR")
    print("="*80)
    
    # Configuration - you can modify these
    repo_url = "https://github.com/anthropics/anthropic-sdk-python"
    prompt = "Create a comprehensive tutorial explanation of this repository that would be suitable for a video presentation. Include the main purpose, key features, and how someone would get started using this project."
    
    print(f"Target Repository: {repo_url}")
    print(f"Analysis Prompt: {prompt}\n")
    
    # Step 1: Generate documentation
    print("STEP 1: GENERATING DOCUMENTATION")
    print("-" * 40)
    documentation_result = generate_documentation(repo_url, prompt)
    
    if not documentation_result["success"]:
        print("Application failed at documentation generation step")
        return
    
    # Print the generated documentation
    print("\n" + "="*80)
    print("GENERATED DOCUMENTATION")
    print("="*80)
    print(documentation_result["analysis"])
    print("="*80)
    
    # Print metadata
    print("\nREPOSITORY METADATA:")
    metadata = documentation_result["metadata"]
    print(f"  Repository: {metadata.get('repo_name')}")
    print(f"  Language: {metadata.get('language')}")
    print(f"  Stars: {metadata.get('stars')}")
    print(f"  Total Files: {documentation_result['stats']['total_files']}")
    print(f"  Total Lines: {documentation_result['stats'].get('total_lines', 'N/A')}")
    
    # Step 2: Create video
    print("\n\nSTEP 2: CREATING VIDEO")
    print("-" * 40)
    video_id = create_video_from_documentation(documentation_result)
    
    if video_id:
        print(f"\nSUCCESS! Video created with ID: {video_id}")
    else:
        print("\nFailed to create video")


if __name__ == "__main__":
    main()
