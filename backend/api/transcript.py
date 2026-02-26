import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from services import transcript
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class TranscriptRequest(BaseModel):
    transcript: str

class TranscriptResponse(BaseModel):
    parsed_srt: str

