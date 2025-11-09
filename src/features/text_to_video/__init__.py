"""
Text-to-Video Feature Module

This module provides HeyGen-powered video generation capabilities for creating
codebase tutorials and educational content from text summaries.
"""

from .hey_gen_generator import create_video, check_video_status

__all__ = [
    'create_video',
    'check_video_status'
]