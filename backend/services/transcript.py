import re
from typing import List, Tuple

TIME_RE = re.compile(r"^(\d+):(\d{2})$")

def parse_transcript_to_blocks(raw_text: str) -> List[Tuple[float, str]]:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    blocks = []
    i = 0

    while i < len(lines):
        m = TIME_RE.match(lines[i])
        if not m:
            i += 1
            continue

        minutes = int(m.group(1))
        seconds = int(m.group(2))
        start_time = minutes * 60 + seconds

        i += 1
        text_lines = []
        while i < len(lines) and not TIME_RE.match(lines[i]):
            text_lines.append(lines[i])
            i += 1

        text = " ".join(text_lines)
        blocks.append((start_time, text))

    return blocks

def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def transcript_to_srt(raw_text: str) -> str:
    blocks = parse_transcript_to_blocks(raw_text)
    srt_lines = []

    for i, (start, text) in enumerate(blocks):
        if i + 1 < len(blocks):
            end = blocks[i + 1][0] - 0.2  # slight overlap buffer
        else:
            end = start + 4.0  # fallback duration for last subtitle

        srt_lines.append(
            f"{i+1}\n"
            f"{format_srt_time(start)} --> {format_srt_time(end)}\n"
            f"{text}\n"
        )

    return "\n".join(srt_lines)
