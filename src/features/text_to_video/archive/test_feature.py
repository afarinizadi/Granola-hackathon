#!/usr/bin/env python3
"""
Simple test script for text-to-video feature.
Run this to test the functionality without making actual API calls.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Load environment variables
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

# Import our modules
from video_creator import VideoCreator, VideoCreationRequest

def test_script_generation():
    """Test script generation without API calls."""
    print("🎬 Testing Text-to-Video Script Generation")
    print("=" * 50)
    
    # Get API key (we'll use it for object creation but not actual API calls)
    api_key = os.getenv("HEYGEN_API_KEY", "test-key")
    
    # Sample text that would come from your code summarizer
    sample_text = """
    This is a Flask web application for user management.
    The application has the following key components:
    
    1. app.py - Main Flask application with route definitions
    2. models.py - User model with SQLAlchemy integration
    3. auth.py - Authentication and session management
    4. forms.py - WTForms for input validation
    
    The app provides REST API endpoints for user CRUD operations,
    includes password hashing with bcrypt, and uses Flask-Migrate
    for database migrations. Error handling is implemented throughout.
    """
    
    creator = VideoCreator(api_key)
    
    # Test different tutorial types
    tutorial_types = ["overview", "deep_dive", "walkthrough", "explanation"]
    
    for tutorial_type in tutorial_types:
        print(f"\n📝 Testing {tutorial_type.upper()} tutorial type:")
        print("-" * 30)
        
        request = VideoCreationRequest(
            text_summary=sample_text,
            title=f"Flask App {tutorial_type.title()}",
            tutorial_type=tutorial_type,
            target_audience="developers"
        )
        
        # Generate script preview (no API calls)
        try:
            preview = creator.generate_script_preview(request)
            
            print(f"✅ Title: {preview['title']}")
            print(f"⏱️  Duration: {preview['total_duration']} seconds")
            print(f"📋 Sections: {len(preview['sections'])}")
            
            # Show section details
            for i, section in enumerate(preview['sections'], 1):
                print(f"   {i}. {section['title']} ({section['duration_estimate']}s)")
            
            print(f"🎙️  Introduction: {preview['introduction'][:100]}...")
            print(f"📝 Script length: {len(preview['full_script'])} characters")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def test_mcp_functions():
    """Test MCP integration functions."""
    print("\n🔧 Testing MCP Integration Functions")
    print("=" * 50)
    
    try:
        from video_creator import create_video_tool, create_script_preview_tool
        
        api_key = os.getenv("HEYGEN_API_KEY", "test-key")
        
        # Create MCP tools
        video_tool = create_video_tool(api_key)
        preview_tool = create_script_preview_tool(api_key)
        
        print(f"✅ Video creation tool: {video_tool.__name__}")
        print(f"✅ Script preview tool: {preview_tool.__name__}")
        
        # Test script preview tool
        sample_text = "Simple Python script that processes data from CSV files."
        
        result = preview_tool(sample_text, tutorial_type="overview")
        print(f"✅ Preview tool test successful - generated script with {len(result['sections'])} sections")
        
    except Exception as e:
        print(f"❌ MCP test error: {e}")

def main():
    """Run all tests."""
    print("🚀 Text-to-Video Feature Test Suite")
    print("=" * 60)
    
    # Check if API key is available
    api_key = os.getenv("HEYGEN_API_KEY")
    if api_key and api_key != "your_heygen_api_key_here":
        print(f"✅ HeyGen API key found: {api_key[:10]}...")
    else:
        print("⚠️  No API key found - testing with mock key")
    
    # Run tests
    test_script_generation()
    test_mcp_functions()
    
    print("\n🎉 All tests completed!")
    print("\nNext steps:")
    print("1. To create actual videos, uncomment the video creation code in example_usage.py")
    print("2. Make sure your HeyGen API key has sufficient credits")
    print("3. Check the generated scripts and adjust settings as needed")

if __name__ == "__main__":
    main()