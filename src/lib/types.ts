export type NetworkType = "farcaster" | "bluesky" | "mastodon"

export type PostStatus = "draft" | "scheduled" | "published" | "failed"

export interface Post {
  id: string
  content: string
  networks: NetworkType[]
  status: PostStatus
  scheduledFor?: Date
  publishedAt?: Date
  createdAt: Date
  updatedAt: Date
  mediaUrls?: string[]
  analytics?: PostAnalytics
  queuePosition?: number
}

export interface PostAnalytics {
  views?: number
  likes?: number
  reposts?: number
  replies?: number
  clicks?: number
  engagement?: number
}

export interface QueueSettings {
  enabled: boolean
  frequency: "hourly" | "daily" | "custom"
  customInterval?: number // minutes
  timeSlots?: string[] // e.g., ['09:00', '14:00', '18:00']
  pauseBetween?: boolean
}
