import type { Post } from "./types"
import { subDays, subHours } from "date-fns"

export function generateDemoAnalytics(): Post[] {
  const demoContent = [
    "Just shipped a new feature! Check out our latest update on multi-network posting.",
    "Building in public is so rewarding. Here's what we learned this week...",
    "Hot take: The future of social media is decentralized and interoperable.",
    "Quick tip: Always schedule your posts during peak engagement hours!",
    "New blog post: Why cross-posting is essential for content creators in 2025",
    "Behind the scenes look at how we're building this platform",
    "Community milestone: We just hit 1000 users! Thank you all!",
    "Pro tip for content creators: Batch create your content for the week ahead",
    "The decentralized web is here, and it's more accessible than ever",
    "What's your favorite social network and why? Drop your thoughts below!",
  ]

  const networks: Array<"farcaster" | "bluesky" | "mastodon"> = ["farcaster", "bluesky", "mastodon"]

  return demoContent.map((content, index) => ({
    id: `demo-${index}`,
    content,
    networks: [networks[index % 3], networks[(index + 1) % 3]],
    status: "published" as const,
    publishedAt: subHours(subDays(new Date(), Math.floor(index * 2.5)), index * 3),
    createdAt: subDays(new Date(), index * 3),
    updatedAt: subDays(new Date(), index * 3),
    analytics: {
      views: Math.floor(Math.random() * 5000) + 500,
      likes: Math.floor(Math.random() * 300) + 50,
      reposts: Math.floor(Math.random() * 100) + 10,
      replies: Math.floor(Math.random() * 50) + 5,
      engagement: Math.floor(Math.random() * 400) + 100,
    },
  }))
}
