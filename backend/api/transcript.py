from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.transcript import save_transcript
from fastapi.responses import FileResponse
from utils import paths

router = APIRouter()

class TranscriptRequest(BaseModel):
    video_id: str
    transcript: str

class TranscriptResponse(BaseModel):
    json_path: str
    vtt_path: str

@router.post("/convert", response_model=TranscriptResponse)
def convert_transcript(req: TranscriptRequest):
    
    try:
        return save_transcript(req.transcript, req.video_id)
    except:
        raise Exception("Could not parse transcript.") 


@router.get("/json/{video_id}")
def get_transcript_json(video_id: str):
    path = paths.SUBS_STORAGE / f"{video_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Transcript not found")
    return FileResponse(path)

@router.get("/vtt/{video_id}")
def get_transcript_vtt(video_id: str):
    path = paths.SUBS_STORAGE / f"{video_id}.vtt"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Transcript not found")
    return FileResponse(path)