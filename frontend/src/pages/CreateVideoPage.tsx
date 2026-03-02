import { useState } from "react"
import { useNavigate } from "react-router-dom"
import type { LanguageConfig } from "../types/language"

const presets: LanguageConfig[] = [
  { id: "1", name: "Spanish → English", fromLang: "Spanish", toLang: "English" },
  { id: "2", name: "Japanese → English", fromLang: "Japanese", toLang: "English" }
]

export default function CreateVideoPage() {
  const navigate = useNavigate()

  const [url, setUrl] = useState("")
  const [transcript, setTranscript] = useState("")
  const [selectedPreset, setSelectedPreset] = useState<LanguageConfig>(presets[0])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleCreate() {
    if (!url || !transcript) {
      setError("Please provide both YouTube URL and transcript.")
      return
    }

    setLoading(true)
    setError(null)

    try {
      // 1️⃣ Download video
      const videoRes = await fetch("http://127.0.0.1:8000/api/video/load", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ youtube_url: url })
      })

      if (!videoRes.ok) throw new Error("Video download failed")

      const videoData = await videoRes.json()
      const videoId = videoData.video_id

      // 2️⃣ Convert transcript
      const transcriptRes = await fetch("http://127.0.0.1:8000/api/transcript/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          video_id: videoId,
          transcript
        })
      })

      if (!transcriptRes.ok) throw new Error("Transcript conversion failed")

      const transcriptData = await transcriptRes.json()
      console.log("Transcript saved:", transcriptData)

      // 3️⃣ Navigate to video page
      navigate(`/video/${videoId}`, {
        state: {
            fromLang: selectedPreset.fromLang,
            toLang: selectedPreset.toLang
        }
        })

    } catch (err: any) {
      setError(err.message || "Failed to create video")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 32, maxWidth: 800, margin: "0 auto" }}>
      <h1>Create New Video</h1>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <label>YouTube URL</label>
        <input
          value={url}
          onChange={e => setUrl(e.target.value)}
          placeholder="https://youtube.com/watch?v=..."
        />

        <label>Paste Transcript</label>
        <textarea
          rows={8}
          value={transcript}
          onChange={e => setTranscript(e.target.value)}
          placeholder="Paste YouTube transcript here..."
        />

        <label>Language Configuration</label>
        <select
          value={selectedPreset.id}
          onChange={e => {
            const preset = presets.find(p => p.id === e.target.value)!
            setSelectedPreset(preset)
          }}
        >
          {presets.map(preset => (
            <option key={preset.id} value={preset.id}>
              {preset.name}
            </option>
          ))}
        </select>

        {error && <div style={{ color: "red" }}>{error}</div>}

        <button onClick={handleCreate} disabled={loading}>
          {loading ? "Processing..." : "Create Video"}
        </button>
      </div>
    </div>
  )
}