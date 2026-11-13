"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/textarea"
import { Checkbox } from "@/components/ui/checkbox"
import type { NetworkType, Post } from "@/lib/types"
import { format } from "date-fns"

interface ScheduleDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  selectedDate?: Date
  post?: Post
  onSchedule: (content: string, networks: NetworkType[], scheduledFor: Date) => void
}

const networkOptions: { value: NetworkType; label: string; color: string }[] = [
  { value: "farcaster", label: "Farcaster", color: "bg-purple-500" },
  { value: "bluesky", label: "BlueSky", color: "bg-blue-500" },
  { value: "mastodon", label: "Mastodon", color: "bg-indigo-500" },
]

export function ScheduleDialog({ open, onOpenChange, selectedDate, post, onSchedule }: ScheduleDialogProps) {
  const [content, setContent] = useState(post?.content || "")
  const [networks, setNetworks] = useState<NetworkType[]>(post?.networks || ["farcaster"])
  const [date, setDate] = useState(selectedDate ? format(selectedDate, "yyyy-MM-dd") : format(new Date(), "yyyy-MM-dd"))
  const [time, setTime] = useState(selectedDate ? format(selectedDate, "HH:mm") : "09:00")

  const toggleNetwork = (network: NetworkType) => {
    setNetworks((prev) => (prev.includes(network) ? prev.filter((n) => n !== network) : [...prev, network]))
  }

  const handleSchedule = () => {
    if (!content.trim() || !date || !time) return

    const scheduledFor = new Date(`${date}T${time}`)
    onSchedule(content, networks, scheduledFor)
    onOpenChange(false)
    setContent("")
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Schedule Post</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <Label htmlFor="schedule-content">Post Content</Label>
            <Input
              id="schedule-content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="What would you like to post?"
              className="min-h-32 mt-2"
              maxLength={280}
            />
            <div className="text-sm text-muted-foreground mt-1">{content.length} / 280 characters</div>
          </div>

          <div>
            <Label className="mb-3 block">Networks</Label>
            <div className="flex flex-wrap gap-3">
              {networkOptions.map(({ value, label, color }) => (
                <label key={value} className="flex items-center gap-2 cursor-pointer">
                  <Checkbox checked={networks.includes(value)} onCheckedChange={() => toggleNetwork(value)} />
                  <div className="flex items-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${color}`} />
                    <span className="text-sm font-medium">{label}</span>
                  </div>
                </label>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="schedule-date">Date</Label>
              <input
                type="date"
                id="schedule-date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full mt-1 px-3 py-2 border rounded-md"
                min={format(new Date(), "yyyy-MM-dd")}
              />
            </div>
            <div>
              <Label htmlFor="schedule-time">Time</Label>
              <input
                type="time"
                id="schedule-time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                className="w-full mt-1 px-3 py-2 border rounded-md"
              />
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSchedule} disabled={!content.trim() || !date || !time || networks.length === 0}>
            Schedule Post
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
