import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from backend.services.transcript import transcript_to_srt

router = APIRouter()

class TranscriptRequest(BaseModel):
    video_id: str
    transcript: str

class TranscriptResponse(BaseModel):
    parsed_srt_path: str

@router.post("/convert", response_model=TranscriptResponse)
def convert_transcript(req: TranscriptRequest):
    
    try:
        return transcript_to_srt(req.transcript)
    except:
        raise Exception("Could not parse transcript to SRT.") 
