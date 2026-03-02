import { useEffect, useState } from "react"
import { useParams, useLocation } from "react-router-dom"
import type { TranscriptResponse } from "../types/transcript"

export default function VideoPage() {
  const { videoId } = useParams()
  const location = useLocation()
  const { fromLang, toLang } = (location.state || {}) as any

  const [transcript, setTranscript] = useState<TranscriptResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/transcript/json/${videoId}`)
      .then(res => res.json())
      .then(data => {
        setTranscript(data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [videoId])

  function handleTokenClick(token: string, context: string) {
    console.log({
      word: token,
      context
    })

    // 🔜 later:
    // POST /api/llm/translate
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      
      {/* Video */}
      <div style={{ padding: 16, borderBottom: "1px solid #ddd" }}>
        <video controls style={{ width: "100%", maxHeight: 360 }}>
          <source src={`http://127.0.0.1:8000/api/video/stream/${videoId}`} />
        </video>
      </div>

      {/* Toolbar */}
      <div style={{ padding: 12, borderBottom: "1px solid #ddd", display: "flex", gap: 12 }}>
        <div>{fromLang} → {toLang}</div>
        <button>Export Anki</button>
        <button>Settings</button>
      </div>

      {/* Main Layout */}
      <div style={{ display: "flex", flex: 1 }}>
        
        {/* Transcript */}
        <div style={{ flex: 2, padding: 16, overflowY: "auto" }}>
          <h3>Transcript</h3>

          {loading && <p>Loading transcript...</p>}

          {transcript?.segments.map(seg => (
            <p key={seg.id}>
              {seg.tokens.map((token, i) => (
                <span
                  key={i}
                  onClick={() => handleTokenClick(token, seg.text)}
                  style={{ cursor: "pointer", marginRight: 4 }}
                >
                  {token}
                </span>
              ))}
            </p>
          ))}
        </div>

        {/* LLM Panel */}
        <div style={{ flex: 1, padding: 16, borderLeft: "1px solid #ddd" }}>
          <h3>Word Info</h3>
          <p>Click a word to translate</p>
        </div>

      </div>
    </div>
  )
}