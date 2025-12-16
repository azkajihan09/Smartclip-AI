# Smartclip AI Configuration
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"
WATERMARKS_DIR = BASE_DIR / "watermarks"

# Ensure directories exist
for directory in [TEMP_DIR, OUTPUT_DIR, MODELS_DIR, WATERMARKS_DIR]:
    directory.mkdir(exist_ok=True)

# Video processing settings
VIDEO_SETTINGS = {
    'max_duration': 3600,  # 1 hour max
    'min_clip_duration': 5,  # 5 seconds minimum
    'max_clip_duration': 60,  # 1 minute maximum
    'default_quality': '720p',
    'fps': 30,
    'audio_sample_rate': 44100
}

# AI Model settings
AI_SETTINGS = {
    'face_detection_confidence': 0.6,
    'face_tracking_threshold': 0.7,
    'speech_detection_threshold': 0.5,
    'silence_threshold': -40,  # dB
    'min_speech_duration': 2.0,  # seconds
    'whisper_model': 'base',  # base, small, medium, large
    'speaker_embedding_model': 'speechbrain/spkrec-ecapa-voxceleb'
}

# Best moments detection settings
MOMENT_DETECTION = {
    'energy_threshold': 0.3,
    'face_prominence_weight': 0.3,
    'audio_quality_weight': 0.4,
    'speech_clarity_weight': 0.3,
    'scene_change_sensitivity': 0.6,
    'highlight_duration': 30  # seconds
}

# Subtitle settings
SUBTITLE_SETTINGS = {
    'font_size': 20,
    'font_color': 'white',
    'background_color': 'black',
    'background_opacity': 0.7,
    'position': 'bottom',
    'margin': 50,
    'max_chars_per_line': 50
}

# Watermark settings
WATERMARK_SETTINGS = {
    'default_position': 'bottom-right',
    'opacity': 0.8,
    'size_percentage': 0.1,  # 10% of video size
    'margin': 20
}

# Podcast split settings
PODCAST_SETTINGS = {
    'split_ratio': 0.5,  # 50-50 split
    'transition_duration': 0.5,  # seconds
    'speaker_switch_threshold': 3.0,  # seconds
    'face_crop_padding': 0.2  # 20% padding around face
}

# Processing settings
PROCESSING = {
    'max_workers': 4,
    'gpu_acceleration': True,
    'batch_size': 8,
    'cache_embeddings': True,
    'temp_cleanup': True
}

# File formats
SUPPORTED_FORMATS = {
    'input': ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v'],
    'output': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav', '.aac', '.flac'],
    'subtitle': ['.srt', '.vtt', '.ass']
}

# Default themes for GUI
GUI_THEMES = {
    'default': {
        'bg_color': '#2b2b2b',
        'fg_color': '#ffffff',
        'button_color': '#404040',
        'accent_color': '#0078d4'
    },
    'dark': {
        'bg_color': '#1e1e1e',
        'fg_color': '#ffffff',
        'button_color': '#333333',
        'accent_color': '#007acc'
    },
    'light': {
        'bg_color': '#f0f0f0',
        'fg_color': '#000000',
        'button_color': '#e1e1e1',
        'accent_color': '#0066cc'
    }
}