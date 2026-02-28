from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.capture_frame import capture_frame

router = APIRouter()


class FrameRequest(BaseModel):
    video_id: str
    time_stamp: float

class FrameResponse(BaseModel):
    frame_path: str


@router.post("/frame")
def get_video_frame(req: FrameRequest):
    frame_path = capture_frame(req.video_id, req.time_stamp)
    return {"frame_path": frame_path}