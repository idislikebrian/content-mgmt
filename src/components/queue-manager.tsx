"use client";

import { useState } from "react";
import type { Post, QueueSettings, NetworkType } from "@/lib/types";
import { PostStore } from "@/lib/store";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

import {
  Clock,
  Plus,
  Trash2,
  GripVertical,
  Play,
  Pause,
} from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import styles from "./queue-manager.module.css";

interface QueueManagerProps {
  posts: Post[];
  onUpdatePost: (id: string, updates: Partial<Post>) => void;
}

const networkColors: Record<NetworkType, string> = {
  farcaster: styles.farcaster,
  bluesky: styles.bluesky,
  mastodon: styles.mastodon,
};

export function QueueManager({ posts, onUpdatePost }: QueueManagerProps) {
  const [settings, setSettings] = useState<QueueSettings>(() =>
    PostStore.getQueueSettings()
  );
  const [newTimeSlot, setNewTimeSlot] = useState("");

  const draftPosts = posts.filter((p) => p.status === "draft");
  const queuedPosts = posts
    .filter((p) => p.queuePosition !== undefined)
    .sort((a, b) => (a.queuePosition ?? 0) - (b.queuePosition ?? 0));

  const updateSettings = (updates: Partial<QueueSettings>) => {
    const next = { ...settings, ...updates };
    setSettings(next);
    PostStore.saveQueueSettings(next);
  };

  const addTimeSlot = () => {
    if (!newTimeSlot) return;
    const timeSlots = [...(settings.timeSlots || []), newTimeSlot].sort();
    updateSettings({ timeSlots });
    setNewTimeSlot("");
  };

  const removeTimeSlot = (slot: string) => {
    updateSettings({
      timeSlots: (settings.timeSlots || []).filter((s) => s !== slot),
    });
  };

  const removeFromQueue = (postId: string) => {
    onUpdatePost(postId, { queuePosition: undefined });
  };

  const moveInQueue = (postId: string, direction: "up" | "down") => {
    const index = queuedPosts.findIndex((p) => p.id === postId);
    if (index === -1) return;

    const swapIndex = direction === "up" ? index - 1 : index + 1;
    if (!queuedPosts[swapIndex]) return;

    const current = queuedPosts[index];
    const swap = queuedPosts[swapIndex];

    onUpdatePost(current.id, { queuePosition: swap.queuePosition });
    onUpdatePost(swap.id, { queuePosition: current.queuePosition });
  };

  return (
    <div className={styles.wrapper}>
      <Card className={styles.settingsCard}>
        <div className={styles.settingsHeader}>
          <div>
            <h3>Queue Settings</h3>
            <p>Configure automatic posting schedule</p>
          </div>

          <div className={styles.toggle}>
            <Switch
              checked={settings.enabled}
              onCheckedChange={(enabled) => updateSettings({ enabled })}
            />
            <Label>{settings.enabled ? "Active" : "Paused"}</Label>
          </div>
        </div>

        <Button
          size="sm"
          variant="outline"
          onClick={async () => {
            await fetch("/api/queue/run", { method: "POST" });
          }}
        >
          Run Queue Now
        </Button>

        <div className={styles.controls}>
          <Label>Posting Frequency</Label>
          <Select
            value={settings.frequency}
            onValueChange={(frequency) => updateSettings({ frequency })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="hourly">Hourly</SelectItem>
              <SelectItem value="daily">Daily</SelectItem>
              <SelectItem value="custom">Custom</SelectItem>
            </SelectContent>
          </Select>

          {settings.frequency === "custom" && (
            <div className={styles.timeSlots}>
              <div className={styles.addSlot}>
                <Input
                  type="time"
                  value={newTimeSlot}
                  onChange={(e) => setNewTimeSlot(e.target.value)}
                />
                <Button size="sm" onClick={addTimeSlot}>
                  <Plus />
                </Button>
              </div>

              <div className={styles.slotList}>
                {(settings.timeSlots || []).map((slot) => (
                  <Badge key={slot}>
                    <Clock />
                    {slot}
                    <button onClick={() => removeTimeSlot(slot)}>
                      <Trash2 />
                    </button>
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      </Card>

      <div className={styles.columns}>
        <Card>
          <h3>Drafts</h3>
          {draftPosts.length === 0 ? (
            <p className={styles.empty}>No drafts</p>
          ) : (
            draftPosts.map((post) => (
              <div key={post.id} className={styles.postRow}>
                <div className={styles.networks}>
                  {post.networks.map((n) => (
                    <span key={n} className={networkColors[n]} />
                  ))}
                </div>
                <p>{post.content}</p>
              </div>
            ))
          )}
        </Card>

        <Card>
          <div className={styles.queueHeader}>
            <h3>Queue ({queuedPosts.length})</h3>
            {settings.enabled ? (
              <Badge>
                <Play /> Active
              </Badge>
            ) : (
              <Badge variant="secondary">
                <Pause /> Paused
              </Badge>
            )}
          </div>

          {queuedPosts.length === 0 ? (
            <p className={styles.empty}>Queue is empty</p>
          ) : (
            queuedPosts.map((post, index) => (
              <div key={post.id} className={styles.queueRow}>
                <button
                  onClick={() => moveInQueue(post.id, "up")}
                  disabled={index === 0}
                >
                  <GripVertical />
                </button>

                <span className={styles.index}>{index + 1}</span>

                <p>{post.content}</p>

                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => removeFromQueue(post.id)}
                >
                  <Trash2 />
                </Button>
              </div>
            ))
          )}
        </Card>
      </div>
    </div>
  );
}
