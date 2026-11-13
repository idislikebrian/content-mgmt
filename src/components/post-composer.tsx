"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import type { NetworkType } from "@/lib/types";
import { Card } from "@/components/ui/card";

import styles from "./post-composer.module.css";

interface PostComposerProps {
  onSave: (
    content: string,
    networks: NetworkType[],
    scheduledFor?: Date
  ) => void;

  onPostNow?: (content: string, networks: NetworkType[]) => Promise<void>;
  onAddToQueue?: (content: string, networks: NetworkType[]) => void;

  initialContent?: string;
  initialNetworks?: NetworkType[];
}

const networkOptions: {
  value: NetworkType;
  label: string;
  dotClass: string;
}[] = [
  {
    value: "farcaster",
    label: "Farcaster",
    dotClass: styles.networkDotFarcaster,
  },
  { value: "bluesky", label: "BlueSky", dotClass: styles.networkDotBluesky },
  { value: "mastodon", label: "Mastodon", dotClass: styles.networkDotMastodon },
];

export function PostComposer({
  onSave,
  onPostNow,
  onAddToQueue,
  initialContent = "",
  initialNetworks = [],
}: PostComposerProps) {
  const [content, setContent] = useState(initialContent);
  const [networks, setNetworks] = useState<NetworkType[]>(
    initialNetworks.length > 0 ? initialNetworks : ["farcaster"]
  );
  const [isScheduling, setIsScheduling] = useState(false);
  const [scheduledDate, setScheduledDate] = useState("");
  const [scheduledTime, setScheduledTime] = useState("");

  const toggleNetwork = (network: NetworkType) => {
    setNetworks((prev) =>
      prev.includes(network)
        ? prev.filter((n) => n !== network)
        : [...prev, network]
    );
  };

  const handleSave = (saveType: "draft" | "schedule") => {
    if (!content.trim()) return;

    let scheduledFor: Date | undefined;

    if (saveType === "schedule" && scheduledDate && scheduledTime) {
      scheduledFor = new Date(`${scheduledDate}T${scheduledTime}`);
    }

    onSave(content, networks, scheduledFor);
    setContent("");
    setIsScheduling(false);
    setScheduledDate("");
    setScheduledTime("");
  };

  const characterCount = content.length;
  const maxChars = 280;
  const exceedsThreshold = characterCount > maxChars * 0.9;

  return (
    <Card className={styles.card}>
      <div className={styles.container}>
        <div>
          <Label htmlFor="content" className={styles.sectionLabel}>
            Post Content
          </Label>
          <Input
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="What's on your mind?"
            className={styles.contentInput}
            maxLength={maxChars}
          />
          <div className={styles.counterRow}>
            <span
              className={`${styles.charCount} ${
                exceedsThreshold ? styles.charCountWarning : ""
              }`}
            >
              {characterCount} / {maxChars}
            </span>
          </div>
        </div>

        <div>
          <Label className={styles.sectionLabel}>Networks</Label>
          <div className={styles.networkList}>
            {networkOptions.map(({ value, label, dotClass }) => (
              <label key={value} className={styles.networkOption}>
                <Checkbox
                  checked={networks.includes(value)}
                  onCheckedChange={() => toggleNetwork(value)}
                />
                <span className={styles.networkChip}>
                  <span className={`${styles.networkDot} ${dotClass}`} />
                  <span>{label}</span>
                </span>
              </label>
            ))}
          </div>
        </div>

        {isScheduling && (
          <div className={styles.scheduleGrid}>
            <div className={styles.scheduleField}>
              <Label htmlFor="date">Date</Label>
              <input
                type="date"
                id="date"
                value={scheduledDate}
                onChange={(e) => setScheduledDate(e.target.value)}
                className={styles.scheduleInput}
                min={new Date().toISOString().split("T")[0]}
              />
            </div>
            <div className={styles.scheduleField}>
              <Label htmlFor="time">Time</Label>
              <input
                type="time"
                id="time"
                value={scheduledTime}
                onChange={(e) => setScheduledTime(e.target.value)}
                className={styles.scheduleInput}
              />
            </div>
          </div>
        )}

        <div className={styles.actions}>
          <Button
            onClick={() => handleSave("draft")}
            variant="outline"
            disabled={!content.trim()}
          >
            Save as Draft
          </Button>

          {!isScheduling ? (
            <Button
              onClick={() => setIsScheduling(true)}
              variant="outline"
              disabled={!content.trim()}
            >
              Schedule
            </Button>
          ) : (
            <>
              <Button
                onClick={() => handleSave("schedule")}
                disabled={!content.trim() || !scheduledDate || !scheduledTime}
              >
                Schedule Post
              </Button>
              <Button onClick={() => setIsScheduling(false)} variant="ghost">
                Cancel
              </Button>
            </>
          )}

          <Button
            onClick={() => {
              if (!content.trim()) return;
              onAddToQueue?.(content, networks);
              setContent("");
            }}
            disabled={!content.trim() || !onAddToQueue}
          >
            Add to Queue
          </Button>

          <Button
            onClick={async () => {
              if (!content.trim()) return;
              await onPostNow?.(content, networks);
              setContent("");
            }}
            disabled={!content.trim() || !onPostNow}
          >
            Post Now
          </Button>
        </div>
      </div>
    </Card>
  );
}
