"use client"

import { useMemo, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import type { Post, NetworkType } from "@/lib/types"
import { BarChart3, TrendingUp, MessageSquare, Repeat2, Eye, Download } from "lucide-react"
import { Bar, BarChart, Line, LineChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import { format, subDays, startOfDay } from "date-fns"

interface AnalyticsDashboardProps {
  posts: Post[]
}

const networkColors: Record<NetworkType, string> = {
  farcaster: "hsl(270, 100%, 60%)",
  bluesky: "hsl(210, 100%, 60%)",
  mastodon: "hsl(240, 100%, 60%)",
}

const networkLabels: Record<NetworkType, string> = {
  farcaster: "Farcaster",
  bluesky: "BlueSky",
  mastodon: "Mastodon",
}

export function AnalyticsDashboard({ posts }: AnalyticsDashboardProps) {
  const [timeRange, setTimeRange] = useState<"7" | "30" | "90">("30")
  const [selectedNetwork, setSelectedNetwork] = useState<NetworkType | "all">("all")

  const publishedPosts = useMemo(() => {
    return posts.filter((p) => p.status === "published" && p.publishedAt)
  }, [posts])

  const filteredPosts = useMemo(() => {
    const days = Number.parseInt(timeRange)
    const cutoffDate = startOfDay(subDays(new Date(), days))

    return publishedPosts.filter((post) => {
      const publishDate = post.publishedAt ? new Date(post.publishedAt) : null
      const isInRange = publishDate && publishDate >= cutoffDate

      if (selectedNetwork === "all") return isInRange
      return isInRange && post.networks.includes(selectedNetwork)
    })
  }, [publishedPosts, timeRange, selectedNetwork])

  const totalMetrics = useMemo(() => {
    return filteredPosts.reduce(
      (acc, post) => {
        const analytics = post.analytics || {}
        return {
          views: acc.views + (analytics.views || 0),
          likes: acc.likes + (analytics.likes || 0),
          reposts: acc.reposts + (analytics.reposts || 0),
          replies: acc.replies + (analytics.replies || 0),
          engagement: acc.engagement + (analytics.engagement || 0),
        }
      },
      { views: 0, likes: 0, reposts: 0, replies: 0, engagement: 0 },
    )
  }, [filteredPosts])

  const networkBreakdown = useMemo(() => {
    const breakdown: Record<string, { posts: number; engagement: number }> = {
      farcaster: { posts: 0, engagement: 0 },
      bluesky: { posts: 0, engagement: 0 },
      mastodon: { posts: 0, engagement: 0 },
    }

    filteredPosts.forEach((post) => {
      post.networks.forEach((network) => {
        breakdown[network].posts += 1
        breakdown[network].engagement += post.analytics?.engagement || 0
      })
    })

    return Object.entries(breakdown).map(([network, data]) => ({
      network: networkLabels[network as NetworkType],
      posts: data.posts,
      engagement: data.engagement,
    }))
  }, [filteredPosts])

  const timeSeriesData = useMemo(() => {
    const days = Number.parseInt(timeRange)
    const data: Record<string, { date: string; posts: number; engagement: number }> = {}

    for (let i = days - 1; i >= 0; i--) {
      const date = startOfDay(subDays(new Date(), i))
      const dateStr = format(date, "MMM d")
      data[dateStr] = { date: dateStr, posts: 0, engagement: 0 }
    }

    filteredPosts.forEach((post) => {
      if (!post.publishedAt) return
      const dateStr = format(new Date(post.publishedAt), "MMM d")
      if (data[dateStr]) {
        data[dateStr].posts += 1
        data[dateStr].engagement += post.analytics?.engagement || 0
      }
    })

    return Object.values(data)
  }, [filteredPosts, timeRange])

  const topPosts = useMemo(() => {
    return [...filteredPosts]
      .sort((a, b) => {
        const engagementA = a.analytics?.engagement || 0
        const engagementB = b.analytics?.engagement || 0
        return engagementB - engagementA
      })
      .slice(0, 5)
  }, [filteredPosts])

  const exportData = () => {
    const csv = [
      ["Date", "Content", "Networks", "Views", "Likes", "Reposts", "Replies", "Engagement"],
      ...filteredPosts.map((post) => [
        post.publishedAt ? format(new Date(post.publishedAt), "yyyy-MM-dd") : "",
        post.content.replace(/"/g, '""'),
        post.networks.join(", "),
        post.analytics?.views || 0,
        post.analytics?.likes || 0,
        post.analytics?.reposts || 0,
        post.analytics?.replies || 0,
        post.analytics?.engagement || 0,
      ]),
    ]
      .map((row) => row.map((cell) => `"${cell}"`).join(","))
      .join("\n")

    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `social-analytics-${format(new Date(), "yyyy-MM-dd")}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
          <p className="text-muted-foreground">Track your social media performance</p>
        </div>
        <div className="flex gap-2">
          <Select value={selectedNetwork} onValueChange={(v) => setSelectedNetwork(v as NetworkType | "all")}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Networks</SelectItem>
              <SelectItem value="farcaster">Farcaster</SelectItem>
              <SelectItem value="bluesky">BlueSky</SelectItem>
              <SelectItem value="mastodon">Mastodon</SelectItem>
            </SelectContent>
          </Select>

          <Select value={timeRange} onValueChange={(v) => setTimeRange(v as "7" | "30" | "90")}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
            </SelectContent>
          </Select>

          <Button onClick={exportData} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </Button>
        </div>
      </div>

      <div className="grid md:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Posts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-primary" />
              <span className="text-2xl font-bold">{filteredPosts.length}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Views</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Eye className="w-5 h-5 text-blue-500" />
              <span className="text-2xl font-bold">{totalMetrics.views.toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Likes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-green-500" />
              <span className="text-2xl font-bold">{totalMetrics.likes.toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Reposts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Repeat2 className="w-5 h-5 text-purple-500" />
              <span className="text-2xl font-bold">{totalMetrics.reposts.toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Replies</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-orange-500" />
              <span className="text-2xl font-bold">{totalMetrics.replies.toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Posts Over Time</h3>
          <ChartContainer
            config={{
              posts: { label: "Posts", color: "hsl(var(--primary))" },
            }}
            className="h-64"
          >
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timeSeriesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Line type="monotone" dataKey="posts" stroke="var(--color-posts)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Engagement Over Time</h3>
          <ChartContainer
            config={{
              engagement: { label: "Engagement", color: "hsl(var(--chart-2))" },
            }}
            className="h-64"
          >
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timeSeriesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Line type="monotone" dataKey="engagement" stroke="var(--color-engagement)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Performance by Network</h3>
        <ChartContainer
          config={{
            posts: { label: "Posts", color: "hsl(var(--chart-1))" },
            engagement: { label: "Engagement", color: "hsl(var(--chart-2))" },
          }}
          className="h-64"
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={networkBreakdown}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="network" />
              <YAxis />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Legend />
              <Bar dataKey="posts" fill="var(--color-posts)" />
              <Bar dataKey="engagement" fill="var(--color-engagement)" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Top Performing Posts</h3>
        {topPosts.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            No published posts yet. Publish some content to see analytics!
          </div>
        ) : (
          <div className="space-y-3">
            {topPosts.map((post, index) => (
              <div key={post.id} className="flex items-start gap-3 p-4 rounded-lg border bg-card">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-semibold">
                  {index + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm line-clamp-2 mb-2">{post.content}</p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Eye className="w-3 h-3" />
                      {post.analytics?.views || 0} views
                    </span>
                    <span className="flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      {post.analytics?.likes || 0} likes
                    </span>
                    <span className="flex items-center gap-1">
                      <Repeat2 className="w-3 h-3" />
                      {post.analytics?.reposts || 0} reposts
                    </span>
                    <span className="flex items-center gap-1">
                      <MessageSquare className="w-3 h-3" />
                      {post.analytics?.replies || 0} replies
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold">{post.analytics?.engagement || 0}</div>
                  <div className="text-xs text-muted-foreground">engagement</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
