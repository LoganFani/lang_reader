import re
import json
from typing import List, Dict
from utils import paths

TIME_RE = re.compile(r"^(\d+):(\d{2})$")

# Sentence-ending punctuation — covers Spanish, English, Japanese, Chinese
SENTENCE_END_RE = re.compile(r'[.!?。！？]["\'»]?$')


def parse_fragments(raw_text: str) -> List[Dict]:
    """Parse raw YouTube transcript into timestamped text fragments."""
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    fragments = []
    i = 0

    while i < len(lines):
        m = TIME_RE.match(lines[i])
        if not m:
            i += 1
            continue

        start = int(m.group(1)) * 60 + int(m.group(2))
        i += 1

        text_lines = []
        while i < len(lines) and not TIME_RE.match(lines[i]):
            text_lines.append(lines[i])
            i += 1

        text = " ".join(text_lines).strip()
        if text:
            fragments.append({"start": float(start), "text": text})

    return fragments


MAX_WORDS   = 30
MAX_SECONDS = 10.0


def merge_into_sentences(fragments: List[Dict]) -> List[Dict]:
    """
    Merge short timestamped fragments into full sentences.
    Flushes on sentence-ending punctuation, or when the buffer
    exceeds MAX_WORDS or MAX_SECONDS — whichever comes first.
    """
    sentences = []
    buffer_text: List[str] = []
    buffer_start: float | None = None
    idx = 1

    def flush(last_frag_start: float) -> None:
        nonlocal idx, buffer_text, buffer_start
        text = " ".join(buffer_text).strip()
        if not text:
            return
        tokens = text.split()
        sentences.append({
            "id": idx,
            "start": buffer_start,
            "end": None,
            "text": text,
            "tokens": tokens,
        })
        idx += 1
        buffer_text = []
        buffer_start = None

    for frag in fragments:
        if buffer_start is None:
            buffer_start = frag["start"]

        buffer_text.append(frag["text"])
        word_count    = sum(len(t.split()) for t in buffer_text)
        elapsed       = frag["start"] - buffer_start

        hit_punctuation = bool(SENTENCE_END_RE.search(frag["text"]))
        hit_word_cap    = word_count >= MAX_WORDS
        hit_time_cap    = elapsed >= MAX_SECONDS

        if hit_punctuation or hit_word_cap or hit_time_cap:
            flush(frag["start"])

    # Flush any remaining buffer
    if buffer_text and buffer_start is not None:
        flush(buffer_start)

    # Fill end times
    for i in range(len(sentences)):
        if i + 1 < len(sentences):
            sentences[i]["end"] = sentences[i + 1]["start"] - 0.05
        else:
            sentences[i]["end"] = sentences[i]["start"] + 4.0

    return sentences


def parse_transcript(raw_text: str) -> List[Dict]:
    fragments = parse_fragments(raw_text)
    return merge_into_sentences(fragments)


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

    json_path = paths.SUBS_STORAGE / f"{video_id}.json"
    vtt_path  = paths.SUBS_STORAGE / f"{video_id}.vtt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"video_id": video_id, "segments": segments}, f, ensure_ascii=False, indent=2)

    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write(transcript_to_vtt(segments))

    return {"json_path": str(json_path), "vtt_path": str(vtt_path)}