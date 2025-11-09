"""
Text-to-Video Feature Module

This module provides HeyGen-powered video generation capabilities for creating
codebase tutorials and educational content from text summaries.
"""

from .heygen_client import HeyGenClient
from .tutorial_generator import TutorialGenerator
from .video_creator import VideoCreator

__all__ = [
    'HeyGenClient',
    'TutorialGenerator',
    'VideoCreator'
]