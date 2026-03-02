import subprocess
from utils import paths

VIDEO_DIR = paths.VIDEO_STORAGE
SUBS_DIR = paths.SUBS_STORAGE

def has_ytdlp() -> bool:
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def download_video(url: str) -> str:
    if not has_ytdlp():
        raise RuntimeError("yt-dlp is not installed")
    
    ytdlp_cmd = [
        "yt-dlp",
        "-P", str(VIDEO_DIR),
        "-f", "bv*[vcodec^=avc1]+ba[acodec^=mp4a]/b",
        "--merge-output-format", "mp4",
        "-o", "%(id)s.%(ext)s",
        "--print", "id",            # <--- This tells yt-dlp to output the ID
        "--no-simulate",            # <--- Ensures it still downloads while printing
        "--ignore-errors",
        "--no-abort-on-error",
        url,
    ]

    # Use capture_output=True to grab the printed ID
    result = subprocess.run(ytdlp_cmd, check=True, capture_output=True, text=True)
    
    # Extract the ID from the output (it will be the first line)
    video_id = result.stdout.strip()
    
    return video_id