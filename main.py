import os
import sys
from yt_download.dependencies import setup_ffmpeg
from pathlib import Path

url = sys.argv[1]

base_dir = Path(__file__).parent
ffmpeg_dir = base_dir / "ffmpeg"

download_dependency = not ffmpeg_dir.exists()
setup_ffmpeg(dir=ffmpeg_dir, download_dependency=download_dependency)

os.system(f'yt-dlp -f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" "{url}"')
