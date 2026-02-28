import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from backend.services.transcript import save_transcript_as_srt

router = APIRouter()

class TranscriptRequest(BaseModel):
    video_id: str
    transcript: str

class TranscriptResponse(BaseModel):
    parsed_srt_path: str

@router.post("/convert", response_model=TranscriptResponse)
def convert_transcript(req: TranscriptRequest):
    
    try:
        return {"parsed_srt_path": save_transcript_as_srt(req.transcript, req.video_id)}
    except:
        raise Exception("Could not parse transcript to SRT.") 
