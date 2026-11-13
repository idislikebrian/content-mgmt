"use client";

import { useState } from "react";
import type { Post, PostStatus, NetworkType } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { format } from "date-fns";

import styles from "./post-library.module.css";

interface PostLibraryProps {
  posts: Post[];
  onDelete: (id: string) => void;
  onEdit: (post: Post) => void;
  onSchedule: (post: Post) => void;
}

const statusClasses: Record<PostStatus, string> = {
  draft: styles.statusDraft,
  scheduled: styles.statusScheduled,
  published: styles.statusPublished,
  failed: styles.statusFailed,
};

const networkClasses: Record<NetworkType, string> = {
  farcaster: styles.networkFarcaster,
  bluesky: styles.networkBluesky,
  mastodon: styles.networkMastodon,
};

const networkLabels: Record<NetworkType, string> = {
  farcaster: "Farcaster",
  bluesky: "BlueSky",
  mastodon: "Mastodon",
};

export function PostLibrary({
  posts,
  onDelete,
  onEdit,
  onSchedule,
}: PostLibraryProps) {
  const [filter, setFilter] = useState<PostStatus | "all">("all");

  const filteredPosts =
    filter === "all" ? posts : posts.filter((p) => p.status === filter);

  return (
    <div className={styles.container}>
      <div className={styles.filterRow}>
        <Button
          variant={filter === "all" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("all")}
        >
          All ({posts.length})
        </Button>
        <Button
          variant={filter === "draft" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("draft")}
        >
          Drafts ({posts.filter((p) => p.status === "draft").length})
        </Button>
        <Button
          variant={filter === "scheduled" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("scheduled")}
        >
          Scheduled ({posts.filter((p) => p.status === "scheduled").length})
        </Button>
        <Button
          variant={filter === "published" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("published")}
        >
          Published ({posts.filter((p) => p.status === "published").length})
        </Button>
      </div>

      <div className="space-y-3">
        {filteredPosts.length === 0 ? (
          <Card>
            No posts found. Create your first post to get started!
          </Card>
        ) : (
          filteredPosts.map((post) => (
            <Card key={post.id} className={styles.postCard}>
              <div className={styles.cardBody}>
                <div className={styles.cardContent}>
                  <div className={styles.badgeRow}>
                    <Badge
                      variant="secondary"
                      className={`${styles.statusBadge} ${statusClasses[post.status]}`}
                    >
                      {post.status}
                    </Badge>
                    {post.networks.map((network) => (
                      <div
                        key={network}
                        className={`${styles.networkPill} ${networkClasses[network]}`}
                      >
                        {networkLabels[network]}
                      </div>
                    ))}
                  </div>

                  <p className={styles.postContent}>{post.content}</p>

                  <div className={styles.infoRow}>
                    {post.scheduledFor && (
                      <span className={styles.metaItem}>
                        {format(post.scheduledFor, "MMM d, yyyy h:mm a")}
                      </span>
                    )}
                    {post.publishedAt && (
                      <span>
                        Published {format(post.publishedAt, "MMM d, yyyy")}
                      </span>
                    )}
                    {!post.scheduledFor && !post.publishedAt && (
                      <span>
                        Created {format(post.createdAt, "MMM d, yyyy")}
                      </span>
                    )}
                  </div>
                </div>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      More
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    {post.status === "draft" && (
                      <>
                        <DropdownMenuItem onClick={() => onEdit(post)}>
                          Edit
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => onSchedule(post)}>
                          Schedule
                        </DropdownMenuItem>
                      </>
                    )}
                    <DropdownMenuItem
                      onClick={() => onDelete(post.id)}
                      className={styles.deleteAction}
                    >
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
