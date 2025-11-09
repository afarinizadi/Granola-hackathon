"""
Example usage of the Text-to-Video feature for creating codebase tutorials.

This example shows how to integrate the text-to-video functionality
with your existing code summarizer and prepare it for MCP server integration.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Load environment variables from .env file
def load_env():
    env_file = current_dir.parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load environment
load_env()

# Import your code summarizer (adjust import path as needed)
# from ..code_summarizer import CodeSummarizer

from video_creator import VideoCreator, VideoCreationRequest
from tutorial_generator import TutorialType


async def create_tutorial_from_codebase():
    """
    Example: Create a tutorial video from codebase analysis.
    """
    # Initialize HeyGen API key (set this in your environment)
    heygen_api_key = os.getenv("HEYGEN_API_KEY")
    if not heygen_api_key:
        print("Please set HEYGEN_API_KEY environment variable")
        return
    
    # Example text from your code summarizer
    # In practice, this would come from your code_summarizer feature
    code_summary = """
    This Python application implements a Flask web service for managing user data.
    
    The main entry point is app.py, which sets up the Flask application and defines routes.
    The User model in models.py handles user data with SQLAlchemy ORM integration.
    Authentication is managed through login and logout endpoints with session management.
    
    Key features include:
    - RESTful API endpoints for user CRUD operations
    - Password hashing and validation
    - Database migrations using Flask-Migrate
    - Error handling with custom exception classes
    - Input validation using Flask-WTF forms
    
    The application follows MVC architecture patterns and includes comprehensive testing.
    """
    
    # Create video creator
    creator = VideoCreator(heygen_api_key)
    
    # Create different types of tutorials
    tutorial_types = [
        ("overview", "Quick Overview"),
        ("deep_dive", "Detailed Analysis"),
        # ("walkthrough", "Code Walkthrough"),
        # ("explanation", "How It Works")
    ]
    
    for tutorial_type, title_prefix in tutorial_types:
        print(f"\n--- Creating {tutorial_type} tutorial ---")
        
        request = VideoCreationRequest(
            text_summary=code_summary,
            title=f"{title_prefix}: Flask User Management App",
            tutorial_type=tutorial_type,
            target_audience="web developers",
            video_style="tutorial"
        )
        
        # First, preview the script
        preview = creator.generate_script_preview(request)
        print(f"Title: {preview['title']}")
        print(f"Estimated duration: {preview['total_duration']} seconds")
        print(f"Number of sections: {len(preview['sections'])}")
        print(f"Introduction: {preview['introduction'][:100]}...")
        
        # Create the actual video
        print("Creating video...")
        result = await creator.create_video(request)
        
        if result.success:
            print(f"✅ Video created successfully!")
            print(f"Video ID: {result.video_id}")
            print(f"Video URL: {result.video_url}")
            print(f"Duration: {result.duration} seconds")
        else:
            print(f"❌ Failed to create video: {result.error_message}")
        
        # Add a small delay between requests to be respectful to the API
        print("Waiting 5 seconds before next video...")
        await asyncio.sleep(5)


async def create_tutorial_from_file():
    """
    Example: Create tutorial from a text file containing code summary.
    """
    heygen_api_key = os.getenv("HEYGEN_API_KEY")
    if not heygen_api_key:
        print("Please set HEYGEN_API_KEY environment variable")
        return
    
    creator = VideoCreator(heygen_api_key)
    
    # Example: create from file (you'd have this from your code summarizer output)
    sample_file_path = "/path/to/code_summary.txt"
    
    if Path(sample_file_path).exists():
        result = await creator.create_video_from_file(
            file_path=sample_file_path,
            tutorial_type="overview",
            title="Codebase Overview Tutorial"
        )
        
        if result.success:
            print(f"Video created from file: {result.video_url}")
        else:
            print(f"Failed: {result.error_message}")
    else:
        print(f"Sample file not found: {sample_file_path}")


def demo_mcp_integration():
    """
    Demonstrate how to integrate with MCP server.
    """
    from video_creator import create_video_tool, create_script_preview_tool
    
    # Create MCP tool functions
    heygen_api_key = os.getenv("HEYGEN_API_KEY", "demo-key")
    
    # These functions can be registered as MCP tools
    video_tool = create_video_tool(heygen_api_key)
    preview_tool = create_script_preview_tool(heygen_api_key)
    
    print("MCP Integration Functions Created:")
    print(f"- Video creation tool: {video_tool.__name__}")
    print(f"- Script preview tool: {preview_tool.__name__}")
    
    # Example MCP server registration (pseudo-code)
    """
    # In your MCP server setup:
    
    @mcp_server.tool()
    async def create_codebase_tutorial(
        text_summary: str,
        title: str = None,
        tutorial_type: str = "overview"
    ):
        return await video_tool(text_summary, title, tutorial_type)
    
    @mcp_server.tool()
    def preview_codebase_tutorial(
        text_summary: str,
        tutorial_type: str = "overview"
    ):
        return preview_tool(text_summary, tutorial_type)
    """


async def test_with_sample_data():
    """
    Test the functionality with sample data.
    """
    # Sample code summary that might come from your code_summarizer
    sample_summaries = {
        "flask_app": """
        Flask web application with user authentication system. 
        Main components: app.py (routes), models.py (User model), 
        auth.py (authentication logic). Uses SQLAlchemy for database,
        Flask-Login for session management, and bcrypt for password hashing.
        """,
        
        "data_pipeline": """
        Python data processing pipeline using pandas and numpy.
        Extracts data from CSV files, performs cleaning and transformation,
        applies statistical analysis, and outputs results to database.
        Includes error handling and logging throughout the process.
        """,
        
        "api_service": """
        RESTful API service built with FastAPI framework.
        Provides endpoints for CRUD operations on user data.
        Includes async database operations, input validation,
        JWT authentication, and comprehensive error handling.
        Uses PostgreSQL database with SQLAlchemy ORM.
        """
    }
    
    heygen_api_key = os.getenv("HEYGEN_API_KEY")
    if not heygen_api_key:
        print("Set HEYGEN_API_KEY environment variable to test video creation")
        heygen_api_key = "demo-key"  # For preview-only testing
    
    creator = VideoCreator(heygen_api_key)
    
    for project_name, summary in sample_summaries.items():
        print(f"\n=== Testing with {project_name} ===")
        
        request = VideoCreationRequest(
            text_summary=summary,
            title=f"{project_name.replace('_', ' ').title()} Tutorial",
            tutorial_type="overview",
            target_audience="developers"
        )
        
        # Generate script preview
        preview = creator.generate_script_preview(request)
        
        print(f"Title: {preview['title']}")
        print(f"Duration: {preview['total_duration']} seconds")
        print(f"Sections: {[s['title'] for s in preview['sections']]}")
        print(f"Script preview: {preview['full_script'][:200]}...")


if __name__ == "__main__":
    print("Text-to-Video Feature Demo")
    print("==========================")
    
    # Run demos
    demo_mcp_integration()
    print()
    
    # Test with sample data
    asyncio.run(test_with_sample_data())
    print()
    
    # Test actual video creation with API calls
    print("🎬 Starting video creation tests...")
    asyncio.run(create_tutorial_from_codebase())