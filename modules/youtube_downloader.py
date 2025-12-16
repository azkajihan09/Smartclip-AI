#!/usr/bin/env python3
"""
YouTube Downloader Module
Download video dari YouTube dengan kualitas terbaik dan metadata lengkap
"""

import yt_dlp
import os
import sys
from pathlib import Path
import logging
from urllib.parse import urlparse, parse_qs
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self, temp_dir=None):
        """Initialize YouTube downloader"""
        self.temp_dir = Path(temp_dir) if temp_dir else Path(__file__).parent.parent / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Default yt-dlp options
        self.ydl_opts = {
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'format': 'best[height<=1080]',  # Max 1080p untuk processing
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['id', 'en'],  # Indonesian dan English
            'embedsubs': False,  # Subtitle terpisah
            'writeinfojson': True,  # Metadata
            'writethumbnail': True,  # Thumbnail
            'ignoreerrors': True,
            'no_warnings': False,
            'extractflat': False,
        }
        
    def validate_url(self, url):
        """Validate YouTube URL"""
        parsed = urlparse(url)
        if parsed.netloc not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            raise ValueError("Invalid YouTube URL")
        return True