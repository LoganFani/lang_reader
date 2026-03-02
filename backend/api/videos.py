from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from backend.services.ytdlp import download_video
from utils import paths

router = APIRouter()

class VideoLoadRequest(BaseModel):
    youtube_url: str

class VideoLoadResponse(BaseModel):
    video_id: str
    status: str
    video_url: str

@router.post("/load", response_model=VideoLoadResponse)
def load_video(req: VideoLoadRequest, background_tasks: BackgroundTasks):
    try:
        video_id = download_video(req.youtube_url)

        video_url = f"http://127.0.0.1:8000/api/video/stream/{video_id}"

        return {
            "video_id": video_id,
            "status": "ready",
            "video_url": video_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stream/{video_id}")
def stream_video(video_id: str):
    video_path = paths.VIDEO_STORAGE / f"{video_id}.mp4"

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(video_path, media_type="video/mp4")