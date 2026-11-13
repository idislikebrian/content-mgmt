"use client"

import { useState, useMemo } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"
import type { Post } from "@/lib/types"
import {
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  eachDayOfInterval,
  format,
  isSameMonth,
  isSameDay,
  addMonths,
  subMonths,
  isToday,
} from "date-fns"

interface CalendarViewProps {
  posts: Post[]
  onDayClick: (date: Date) => void
  onPostClick: (post: Post) => void
}

const networkColors: Record<string, string> = {
  farcaster: "bg-purple-500",
  bluesky: "bg-blue-500",
  mastodon: "bg-indigo-500",
}

export function CalendarView({ posts, onDayClick, onPostClick }: CalendarViewProps) {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [view, setView] = useState<"month" | "week">("month")

  const scheduledPosts = useMemo(() => posts.filter((p) => p.status === "scheduled" && p.scheduledFor), [posts])

  const monthStart = startOfMonth(currentDate)
  const monthEnd = endOfMonth(currentDate)
  const calendarStart = startOfWeek(monthStart)
  const calendarEnd = endOfWeek(monthEnd)
  const calendarDays = eachDayOfInterval({ start: calendarStart, end: calendarEnd })

  const getPostsForDay = (day: Date) => {
    return scheduledPosts.filter((post) => post.scheduledFor && isSameDay(new Date(post.scheduledFor), day))
  }

  const previousMonth = () => setCurrentDate(subMonths(currentDate, 1))
  const nextMonth = () => setCurrentDate(addMonths(currentDate, 1))

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={previousMonth}>
            <ChevronLeft className="w-4 h-4" />
          </Button>
          <h2 className="text-xl font-semibold min-w-48 text-center">{format(currentDate, "MMMM yyyy")}</h2>
          <Button variant="outline" size="sm" onClick={nextMonth}>
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>

        <div className="flex gap-2">
          <Button variant={view === "month" ? "default" : "outline"} size="sm" onClick={() => setView("month")}>
            Month
          </Button>
          <Button variant={view === "week" ? "default" : "outline"} size="sm" onClick={() => setView("week")}>
            Week
          </Button>
        </div>
      </div>

      <Card className="p-4">
        <div className="grid grid-cols-7 gap-2">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
            <div key={day} className="text-center text-sm font-semibold text-muted-foreground py-2">
              {day}
            </div>
          ))}

          {calendarDays.map((day, index) => {
            const dayPosts = getPostsForDay(day)
            const isCurrentMonth = isSameMonth(day, currentDate)
            const isTodayDate = isToday(day)

            return (
              <button
                key={index}
                onClick={() => onDayClick(day)}
                className={`min-h-24 p-2 rounded-lg border transition-colors text-left ${
                  isCurrentMonth ? "bg-card hover:bg-accent" : "bg-muted/30"
                } ${isTodayDate ? "border-primary border-2" : "border-border"}`}
              >
                <div
                  className={`text-sm font-medium mb-1 ${
                    isTodayDate ? "text-primary" : isCurrentMonth ? "text-foreground" : "text-muted-foreground"
                  }`}
                >
                  {format(day, "d")}
                </div>

                <div className="space-y-1">
                  {dayPosts.slice(0, 3).map((post) => (
                    <div
                      key={post.id}
                      onClick={(e) => {
                        e.stopPropagation()
                        onPostClick(post)
                      }}
                      className="text-xs p-1 rounded bg-primary/10 hover:bg-primary/20 transition-colors cursor-pointer line-clamp-1"
                    >
                      <div className="flex items-center gap-1 mb-0.5">
                        {post.networks.map((network) => (
                          <div key={network} className={`w-2 h-2 rounded-full ${networkColors[network]}`} />
                        ))}
                      </div>
                      {post.scheduledFor && format(new Date(post.scheduledFor), "h:mm a")}
                    </div>
                  ))}
                  {dayPosts.length > 3 && (
                    <div className="text-xs text-muted-foreground">+{dayPosts.length - 3} more</div>
                  )}
                </div>
              </button>
            )
          })}
        </div>
      </Card>

      <Card className="p-4">
        <h3 className="font-semibold mb-3">Upcoming Posts</h3>
        <div className="space-y-2">
          {scheduledPosts
            .sort((a, b) => {
              const dateA = a.scheduledFor ? new Date(a.scheduledFor).getTime() : 0
              const dateB = b.scheduledFor ? new Date(b.scheduledFor).getTime() : 0
              return dateA - dateB
            })
            .slice(0, 5)
            .map((post) => (
              <div
                key={post.id}
                onClick={() => onPostClick(post)}
                className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent cursor-pointer transition-colors"
              >
                <div className="flex gap-1 mt-1">
                  {post.networks.map((network) => (
                    <div key={network} className={`w-3 h-3 rounded-full ${networkColors[network]}`} />
                  ))}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm line-clamp-2">{post.content}</p>
                  {post.scheduledFor && (
                    <p className="text-xs text-muted-foreground mt-1">
                      {format(new Date(post.scheduledFor), "MMM d, yyyy 'at' h:mm a")}
                    </p>
                  )}
                </div>
              </div>
            ))}
          {scheduledPosts.length === 0 && (
            <div className="text-center py-8 text-muted-foreground text-sm">
              No scheduled posts yet. Schedule a post to see it here!
            </div>
          )}
        </div>
      </Card>
    </div>
  )
}
