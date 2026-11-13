"use client";

import { useState, useEffect } from "react";
import type { Post, PostStatus, NetworkType } from "@/lib/types";
import { PostStore } from "@/lib/store";

export function usePosts() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setPosts(PostStore.getPosts());
    setLoading(false);
  }, []);

  const addPost = (
    content: string,
    networks: NetworkType[],
    scheduledFor?: Date
  ): Post => {
    const post = PostStore.addPost({
      content,
      networks,
      status: scheduledFor ? "scheduled" : "draft",
      scheduledFor,
    });

    setPosts((prev) => [post, ...prev]);
    return post;
  };

  const updatePost = (id: string, updates: Partial<Post>) => {
    const updated = PostStore.updatePost(id, updates);
    if (updated) {
      setPosts((prev) => prev.map((p) => (p.id === id ? updated : p)));
    }
    return updated;
  };

  const deletePost = (id: string) => {
    PostStore.deletePost(id);
    setPosts((prev) => prev.filter((p) => p.id !== id));
  };

  /**
   * Queue helpers
   */

  const enqueuePost = (id: string) => {
    const queued = posts
      .filter((p) => p.queuePosition !== undefined)
      .sort((a, b) => (a.queuePosition ?? 0) - (b.queuePosition ?? 0));

    const nextPosition =
      queued.length === 0
        ? 1
        : (queued[queued.length - 1].queuePosition ?? 0) + 1;

    return updatePost(id, { queuePosition: nextPosition });
  };

  const dequeuePost = (id: string) => {
    return updatePost(id, { queuePosition: undefined });
  };

  const filterByStatus = (status: PostStatus) => {
    return posts.filter((p) => p.status === status);
  };

  const filterByNetwork = (network: NetworkType) => {
    return posts.filter((p) => p.networks.includes(network));
  };

  return {
    posts,
    loading,

    addPost,
    updatePost,
    deletePost,

    enqueuePost,
    dequeuePost,

    filterByStatus,
    filterByNetwork,

    drafts: posts.filter((p) => p.status === "draft"),
    scheduled: posts.filter((p) => p.status === "scheduled"),
    published: posts.filter((p) => p.status === "published"),
    queued: posts
      .filter((p) => p.queuePosition !== undefined)
      .sort((a, b) => (a.queuePosition ?? 0) - (b.queuePosition ?? 0)),
  };
}
