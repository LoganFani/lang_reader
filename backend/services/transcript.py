import re
import json
from typing import List, Dict
from utils import paths

TIME_RE = re.compile(r"^(\d+):(\d{2})$")


def parse_transcript(raw_text: str) -> List[Dict]:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    segments = []
    i = 0
    idx = 1

    while i < len(lines):
        m = TIME_RE.match(lines[i])
        if not m:
            i += 1
            continue

        minutes = int(m.group(1))
        seconds = int(m.group(2))
        start = minutes * 60 + seconds

        i += 1
        text_lines = []
        while i < len(lines) and not TIME_RE.match(lines[i]):
            text_lines.append(lines[i])
            i += 1

        text = " ".join(text_lines).strip()
        tokens = text.split()

        segments.append({
            "id": idx,
            "start": float(start),
            "end": None,  # fill later
            "text": text,
            "tokens": tokens
        })
        idx += 1

    # Fill end times
    for i in range(len(segments)):
        if i + 1 < len(segments):
            segments[i]["end"] = segments[i + 1]["start"] - 0.05
        else:
            segments[i]["end"] = segments[i]["start"] + 3.0

    return segments


def format_vtt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}"


def transcript_to_vtt(segments: List[Dict]) -> str:
    lines = ["WEBVTT\n"]
    for seg in segments:
        lines.append(
            f"{format_vtt_time(seg['start'])} --> {format_vtt_time(seg['end'])}\n"
            f"{seg['text']}\n"
        )
    return "\n".join(lines)


def save_transcript(raw_text: str, video_id: str) -> Dict[str, str]:
    segments = parse_transcript(raw_text)

    json_payload = {
        "video_id": video_id,
        "segments": segments
    }

    json_path = paths.SUBS_STORAGE / f"{video_id}.json"
    vtt_path = paths.SUBS_STORAGE / f"{video_id}.vtt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, ensure_ascii=False, indent=2)

    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write(transcript_to_vtt(segments))

    return {
        "json_path": str(json_path),
        "vtt_path": str(vtt_path)
    }