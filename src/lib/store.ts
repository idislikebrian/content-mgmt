import type { Post, QueueSettings } from "./types"

const POSTS_KEY = "social_posts"
const QUEUE_KEY = "queue_settings"

export const PostStore = {
  getPosts(): Post[] {
    if (typeof window === "undefined") return []
    const data = localStorage.getItem(POSTS_KEY)
    if (!data) return []
    return JSON.parse(data, (key, value) => {
      if (key === "scheduledFor" || key === "publishedAt" || key === "createdAt" || key === "updatedAt") {
        return value ? new Date(value) : undefined
      }
      return value
    })
  },

  savePosts(posts: Post[]) {
    if (typeof window === "undefined") return
    localStorage.setItem(POSTS_KEY, JSON.stringify(posts))
  },

  addPost(post: Omit<Post, "id" | "createdAt" | "updatedAt">): Post {
    const newPost: Post = {
      ...post,
      id: crypto.randomUUID(),
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    const posts = this.getPosts()
    posts.unshift(newPost)
    this.savePosts(posts)
    return newPost
  },

  updatePost(id: string, updates: Partial<Post>): Post | null {
    const posts = this.getPosts()
    const index = posts.findIndex((p) => p.id === id)
    if (index === -1) return null

    posts[index] = {
      ...posts[index],
      ...updates,
      updatedAt: new Date(),
    }
    this.savePosts(posts)
    return posts[index]
  },

  deletePost(id: string) {
    const posts = this.getPosts().filter((p) => p.id !== id)
    this.savePosts(posts)
  },

  getQueueSettings(): QueueSettings {
    if (typeof window === "undefined") return { enabled: false, frequency: "daily" }
    const data = localStorage.getItem(QUEUE_KEY)
    return data ? JSON.parse(data) : { enabled: false, frequency: "daily" }
  },

  saveQueueSettings(settings: QueueSettings) {
    if (typeof window === "undefined") return
    localStorage.setItem(QUEUE_KEY, JSON.stringify(settings))
  },
}
