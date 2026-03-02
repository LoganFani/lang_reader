from fastapi import FastAPI, BackgroundTasks
from backend.api import videos, llm, transcript, frames
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(videos.router, prefix="/api/video")
app.include_router(llm.router, prefix="/api/llm")
app.include_router(transcript.router, prefix="/api/transcript")
app.include_router(frames.router, prefix="/api/capture")

@app.get("/")
def root():
    return "Hello world"

'''
app.include_router(anki.router, prefix="/api/anki")

'''