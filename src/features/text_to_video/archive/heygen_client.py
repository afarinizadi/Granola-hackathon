"""
HeyGen API Client

Handles communication with HeyGen's API for video generation.
"""

import asyncio
import aiohttp
import json
import ssl
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class VideoQuality(Enum):
    """Video quality options"""
    LOW = "480p"
    MEDIUM = "720p"
    HIGH = "1080p"


class AvatarType(Enum):
    """Available avatar types"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    TECHNICAL = "technical"
    FRIENDLY = "friendly"


@dataclass
class VideoConfig:
    """Configuration for video generation"""
    avatar_id: str
    voice_id: str
    quality: VideoQuality = VideoQuality.MEDIUM
    background: str = "office"
    duration_limit: int = 300  # seconds
    aspect_ratio: str = "16:9"


@dataclass
class VideoRequest:
    """Video generation request"""
    script: str
    title: str
    config: VideoConfig
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class VideoResponse:
    """Video generation response"""
    video_id: str
    status: str
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    error_message: Optional[str] = None


class HeyGenClient:
    """
    Client for interacting with HeyGen API.
    
    This class provides methods to create videos from text scripts
    using HeyGen's AI avatar and voice synthesis capabilities.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.heygen.com/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        # Disable SSL verification to fix macOS certificate issues
        connector = aiohttp.TCPConnector(ssl=False)
        
        self.session = aiohttp.ClientSession(
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            },
            timeout=aiohttp.ClientTimeout(total=300),
            connector=connector
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_avatars(self) -> List[Dict[str, Any]]:
        """
        Get list of available avatars.
        
        Returns:
            List of avatar configurations
        """
        async with self.session.get(f"{self.base_url}/avatars") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("avatars", [])
            else:
                raise Exception(f"Failed to get avatars: {response.status}")
    
    async def get_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of available voices.
        
        Returns:
            List of voice configurations
        """
        async with self.session.get(f"{self.base_url}/voices") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("voices", [])
            else:
                raise Exception(f"Failed to get voices: {response.status}")
    
    async def create_video(self, request: VideoRequest) -> VideoResponse:
        """
        Create a video from text script.
        
        Args:
            request: Video generation request
            
        Returns:
            Video response with job ID and status
        """
        payload = {
            "video_inputs": [{
                "character": {
                    "type": "avatar",
                    "avatar_id": request.config.avatar_id,
                    "scale": 1.0
                },
                "voice": {
                    "type": "text_to_speech",
                    "text": request.script,
                    "voice_id": request.config.voice_id
                },
                "background": {
                    "type": "color",
                    "value": "#ffffff"
                }
            }],
            "dimension": {
                "width": 1920 if request.config.quality == VideoQuality.HIGH else 1280,
                "height": 1080 if request.config.quality == VideoQuality.HIGH else 720
            },
            "aspect_ratio": request.config.aspect_ratio,
            "title": request.title
        }
        
        async with self.session.post(
            f"{self.base_url}/video/generate",
            json=payload
        ) as response:
            data = await response.json()
            
            if response.status == 200:
                # Handle different possible response structures
                video_id = data.get("data", {}).get("video_id") or data.get("video_id")
                if video_id:
                    return VideoResponse(
                        video_id=video_id,
                        status="processing"
                    )
                else:
                    return VideoResponse(
                        video_id="",
                        status="failed",
                        error_message=f"Could not find video_id in response: {data}"
                    )
            else:
                error_msg = data.get("error", {}).get("message") if isinstance(data.get("error"), dict) else str(data.get("error", "Unknown error"))
                return VideoResponse(
                    video_id="",
                    status="failed",
                    error_message=error_msg
                )
    
    async def get_video_status(self, video_id: str) -> VideoResponse:
        """
        Check video generation status.
        
        Args:
            video_id: Video job ID
            
        Returns:
            Updated video response with current status
        """
        async with self.session.get(f"{self.base_url}/video/{video_id}") as response:
            if response.status == 200:
                data = await response.json()
                return VideoResponse(
                    video_id=video_id,
                    status=data.get("status", "unknown"),
                    video_url=data.get("video_url"),
                    thumbnail_url=data.get("thumbnail_url"),
                    duration=data.get("duration")
                )
            else:
                return VideoResponse(
                    video_id=video_id,
                    status="error",
                    error_message=f"Failed to get status: {response.status}"
                )
    
    async def wait_for_completion(self, video_id: str, timeout: int = 600) -> VideoResponse:
        """
        Wait for video generation to complete.
        
        Args:
            video_id: Video job ID
            timeout: Maximum wait time in seconds
            
        Returns:
            Final video response
        """
        start_time = asyncio.get_event_loop().time()
        
        while True:
            response = await self.get_video_status(video_id)
            
            if response.status == "completed":
                return response
            elif response.status == "failed" or response.status == "error":
                return response
            
            # Check timeout
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                return VideoResponse(
                    video_id=video_id,
                    status="timeout",
                    error_message=f"Video generation timed out after {timeout} seconds"
                )
            
            # Wait before next check
            await asyncio.sleep(10)


# Default configurations
DEFAULT_CONFIGS = {
    "tutorial": VideoConfig(
        avatar_id="392983fb140d4baa93c85b31cb6f09cb",
        voice_id="5d8c378ba8c3434586081a52ac368738",
        quality=VideoQuality.HIGH,
        background="tech_office"
    ),
    "explanation": VideoConfig(
        avatar_id="default_professional",
        voice_id="en_us_male_confident",
        quality=VideoQuality.MEDIUM,
        background="modern_office" 
    ),
    "overview": VideoConfig(
        avatar_id="default_friendly",
        voice_id="en_us_female_friendly",
        quality=VideoQuality.MEDIUM,
        background="clean_white"
    )
}