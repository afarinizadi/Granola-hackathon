"""
Video Creator

Main interface for creating educational videos from text summaries using HeyGen.
Designed to be easily integrated into MCP servers.
"""

import asyncio
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from heygen_client import HeyGenClient, VideoConfig, VideoRequest, VideoResponse, DEFAULT_CONFIGS
from tutorial_generator import TutorialGenerator, TutorialType, TutorialScript


@dataclass
class VideoCreationRequest:
    """Request for creating a tutorial video"""
    text_summary: str
    title: Optional[str] = None
    tutorial_type: str = "overview"  # overview, deep_dive, walkthrough, explanation, quick_start
    target_audience: str = "developers"
    video_style: str = "tutorial"  # tutorial, explanation, overview
    include_code_examples: bool = True
    custom_config: Optional[Dict[str, Any]] = None


@dataclass
class VideoCreationResult:
    """Result of video creation process"""
    success: bool
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    script_used: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class VideoCreator:
    """
    Main class for creating educational videos from text summaries.
    
    This class coordinates between text processing and video generation
    to create polished tutorial videos using HeyGen.
    """
    
    def __init__(self, heygen_api_key: str):
        """
        Initialize VideoCreator.
        
        Args:
            heygen_api_key: API key for HeyGen service
        """
        self.heygen_api_key = heygen_api_key
        self.tutorial_generator = TutorialGenerator()
    
    async def create_video(self, request: VideoCreationRequest) -> VideoCreationResult:
        """
        Create a tutorial video from text summary.
        
        Args:
            request: Video creation request with text and preferences
            
        Returns:
            Result containing video information or error details
        """
        try:
            # Validate input
            if not request.text_summary or not request.text_summary.strip():
                return VideoCreationResult(
                    success=False,
                    error_message="Text summary cannot be empty"
                )
            
            # Convert tutorial type string to enum
            try:
                tutorial_type = TutorialType(request.tutorial_type.lower())
            except ValueError:
                tutorial_type = TutorialType.OVERVIEW
            
            # Generate tutorial script
            script = self.tutorial_generator.generate_tutorial(
                text_summary=request.text_summary,
                tutorial_type=tutorial_type,
                title=request.title,
                target_audience=request.target_audience,
                include_code_examples=request.include_code_examples
            )
            
            # Format script for HeyGen
            formatted_script = self.tutorial_generator.format_for_heygen(script)
            
            # Get video configuration
            video_config = self._get_video_config(request.video_style, request.custom_config)
            
            # Create video using HeyGen
            async with HeyGenClient(self.heygen_api_key) as client:
                video_request = VideoRequest(
                    script=formatted_script,
                    title=script.title,
                    config=video_config
                )
                
                # Submit video generation request
                response = await client.create_video(video_request)
                
                if response.status == "processing":
                    # Wait for completion
                    final_response = await client.wait_for_completion(response.video_id)
                    
                    if final_response.status == "completed":
                        return VideoCreationResult(
                            success=True,
                            video_id=final_response.video_id,
                            video_url=final_response.video_url,
                            thumbnail_url=final_response.thumbnail_url,
                            duration=final_response.duration,
                            script_used=formatted_script,
                            metadata={
                                "tutorial_type": request.tutorial_type,
                                "target_audience": request.target_audience,
                                "script_sections": len(script.sections),
                                "estimated_duration": script.total_duration,
                                "actual_duration": final_response.duration
                            }
                        )
                    else:
                        return VideoCreationResult(
                            success=False,
                            error_message=final_response.error_message or f"Video generation failed: {final_response.status}"
                        )
                else:
                    return VideoCreationResult(
                        success=False,
                        error_message=response.error_message or "Failed to start video generation"
                    )
        
        except Exception as e:
            return VideoCreationResult(
                success=False,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    async def create_video_from_file(
        self, 
        file_path: str, 
        tutorial_type: str = "overview",
        title: Optional[str] = None
    ) -> VideoCreationResult:
        """
        Create video from a text file containing code summary.
        
        Args:
            file_path: Path to text file with code summary
            tutorial_type: Type of tutorial to create
            title: Optional custom title
            
        Returns:
            Video creation result
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_summary = f.read()
            
            # Extract title from filename if not provided
            if not title:
                title = Path(file_path).stem.replace('_', ' ').title()
            
            request = VideoCreationRequest(
                text_summary=text_summary,
                title=title,
                tutorial_type=tutorial_type
            )
            
            return await self.create_video(request)
        
        except FileNotFoundError:
            return VideoCreationResult(
                success=False,
                error_message=f"File not found: {file_path}"
            )
        except Exception as e:
            return VideoCreationResult(
                success=False,
                error_message=f"Error reading file: {str(e)}"
            )
    
    def _get_video_config(self, style: str, custom_config: Optional[Dict[str, Any]]) -> VideoConfig:
        """Get video configuration based on style and custom settings."""
        # Start with default config for the style
        base_config = DEFAULT_CONFIGS.get(style, DEFAULT_CONFIGS["tutorial"])
        
        # Apply custom configurations if provided
        if custom_config:
            # Create new config with custom values
            config_dict = asdict(base_config)
            config_dict.update(custom_config)
            
            # Reconstruct VideoConfig object
            return VideoConfig(**config_dict)
        
        return base_config
    
    async def get_available_avatars(self) -> List[Dict[str, Any]]:
        """Get list of available HeyGen avatars."""
        async with HeyGenClient(self.heygen_api_key) as client:
            return await client.get_avatars()
    
    async def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available HeyGen voices."""
        async with HeyGenClient(self.heygen_api_key) as client:
            return await client.get_voices()
    
    def generate_script_preview(self, request: VideoCreationRequest) -> Dict[str, Any]:
        """
        Generate a preview of the tutorial script without creating video.
        
        Args:
            request: Video creation request
            
        Returns:
            Dictionary containing script preview and metadata
        """
        try:
            # Convert tutorial type
            tutorial_type = TutorialType(request.tutorial_type.lower())
        except ValueError:
            tutorial_type = TutorialType.OVERVIEW
        
        # Generate script
        script = self.tutorial_generator.generate_tutorial(
            text_summary=request.text_summary,
            tutorial_type=tutorial_type,
            title=request.title,
            target_audience=request.target_audience,
            include_code_examples=request.include_code_examples
        )
        
        # Format for preview
        formatted_script = self.tutorial_generator.format_for_heygen(script)
        
        return {
            "title": script.title,
            "introduction": script.introduction,
            "sections": [
                {
                    "title": section.title,
                    "content": section.content,
                    "duration_estimate": section.duration_estimate
                }
                for section in script.sections
            ],
            "conclusion": script.conclusion,
            "full_script": formatted_script,
            "total_duration": script.total_duration,
            "metadata": script.metadata
        }


# MCP Server Integration Helper Functions
def create_video_tool(heygen_api_key: str):
    """
    Create a video creation tool function for MCP server integration.
    
    Args:
        heygen_api_key: HeyGen API key
        
    Returns:
        Async function that can be used as MCP tool
    """
    video_creator = VideoCreator(heygen_api_key)
    
    async def create_tutorial_video(
        text_summary: str,
        title: Optional[str] = None,
        tutorial_type: str = "overview",
        target_audience: str = "developers",
        video_style: str = "tutorial"
    ) -> Dict[str, Any]:
        """
        MCP tool function for creating tutorial videos.
        
        Args:
            text_summary: Code summary text to convert to video
            title: Optional video title
            tutorial_type: Type of tutorial (overview, deep_dive, etc.)
            target_audience: Target audience
            video_style: Video style configuration
            
        Returns:
            Dictionary with video creation results
        """
        request = VideoCreationRequest(
            text_summary=text_summary,
            title=title,
            tutorial_type=tutorial_type,
            target_audience=target_audience,
            video_style=video_style
        )
        
        result = await video_creator.create_video(request)
        return asdict(result)
    
    return create_tutorial_video


def create_script_preview_tool(heygen_api_key: str):
    """
    Create a script preview tool function for MCP server integration.
    
    Args:
        heygen_api_key: HeyGen API key
        
    Returns:
        Function that can be used as MCP tool
    """
    video_creator = VideoCreator(heygen_api_key)
    
    def preview_tutorial_script(
        text_summary: str,
        title: Optional[str] = None,
        tutorial_type: str = "overview",
        target_audience: str = "developers"
    ) -> Dict[str, Any]:
        """
        MCP tool function for previewing tutorial scripts.
        
        Args:
            text_summary: Code summary text
            title: Optional video title
            tutorial_type: Type of tutorial
            target_audience: Target audience
            
        Returns:
            Dictionary with script preview
        """
        request = VideoCreationRequest(
            text_summary=text_summary,
            title=title,
            tutorial_type=tutorial_type,
            target_audience=target_audience
        )
        
        return video_creator.generate_script_preview(request)
    
    return preview_tutorial_script


# Example usage
async def main():
    """Example usage of the VideoCreator."""
    # This would normally come from environment variables
    api_key = os.getenv("HEYGEN_API_KEY", "your-api-key-here")
    
    creator = VideoCreator(api_key)
    
    # Example text summary (this would come from your code summarizer)
    sample_text = """
    This application is a Flask-based web service that provides user authentication and data management.
    The main components include a User model with login functionality, a database connection using SQLAlchemy,
    and REST API endpoints for CRUD operations. The application follows MVC architecture patterns and includes
    error handling and input validation.
    """
    
    request = VideoCreationRequest(
        text_summary=sample_text,
        title="Flask Web Service Overview",
        tutorial_type="overview",
        target_audience="web developers"
    )
    
    # Preview script first
    preview = creator.generate_script_preview(request)
    print("Script Preview:")
    print(f"Title: {preview['title']}")
    print(f"Duration: {preview['total_duration']} seconds")
    print(f"Sections: {len(preview['sections'])}")
    
    # Create actual video (uncomment when ready)
    # result = await creator.create_video(request)
    # print(f"Video creation {'successful' if result.success else 'failed'}")
    # if result.success:
    #     print(f"Video URL: {result.video_url}")


if __name__ == "__main__":
    asyncio.run(main())