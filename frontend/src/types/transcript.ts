export interface TranscriptSegment {
  id: number
  start: number
  end: number
  text: string
  tokens: string[]
}


export interface TranscriptResponse {
  video_id: string
  segments: TranscriptSegment[]
}