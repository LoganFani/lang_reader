import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from backend.services.transcript import save_transcript

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
