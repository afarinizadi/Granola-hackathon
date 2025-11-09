"""
Configuration loader for text-to-video feature.
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[str] = None):
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Optional path to .env file. If None, looks for .env in project root.
    """
    if env_path is None:
        # Look for .env file in project root
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent  # Go up to project root
        env_path = project_root / ".env"
    
    env_file = Path(env_path)
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already in environment
                    if key not in os.environ:
                        os.environ[key] = value


class Config:
    """Configuration class for text-to-video feature."""
    
    def __init__(self):
        # Load .env file if it exists
        load_env_file()
        
        # HeyGen API settings
        self.heygen_api_key = os.getenv("HEYGEN_API_KEY")
        self.heygen_base_url = os.getenv("HEYGEN_BASE_URL", "https://api.heygen.com/v2")
        
        # Video settings
        self.default_video_quality = os.getenv("DEFAULT_VIDEO_QUALITY", "720p")
        self.default_avatar_id = os.getenv("DEFAULT_AVATAR_ID", "default_technical")
        self.default_voice_id = os.getenv("DEFAULT_VOICE_ID", "en_us_female_calm")
        self.default_background = os.getenv("DEFAULT_BACKGROUND", "tech_office")
        
        # Tutorial settings
        self.default_tutorial_type = os.getenv("DEFAULT_TUTORIAL_TYPE", "overview")
        self.default_target_audience = os.getenv("DEFAULT_TARGET_AUDIENCE", "developers")
        self.default_speaking_rate = int(os.getenv("DEFAULT_SPEAKING_RATE", "150"))
        
        # MCP settings
        self.mcp_server_port = int(os.getenv("MCP_SERVER_PORT", "3000"))
        self.mcp_server_host = os.getenv("MCP_SERVER_HOST", "localhost")
        
        # Debug settings
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.heygen_api_key:
            print("ERROR: HEYGEN_API_KEY environment variable is required")
            return False
        
        return True
    
    def get_heygen_config(self) -> dict:
        """Get HeyGen-specific configuration."""
        return {
            "api_key": self.heygen_api_key,
            "base_url": self.heygen_base_url,
            "default_avatar_id": self.default_avatar_id,
            "default_voice_id": self.default_voice_id,
            "default_background": self.default_background,
            "default_quality": self.default_video_quality
        }
    
    def get_tutorial_config(self) -> dict:
        """Get tutorial generation configuration."""
        return {
            "default_type": self.default_tutorial_type,
            "default_audience": self.default_target_audience,
            "speaking_rate": self.default_speaking_rate
        }


# Global config instance
config = Config()