import { postToFarcaster } from "@/lib/farcaster";
import { PostStore } from "@/lib/store";
import type { Post } from "@/lib/types";

export async function POST() {
  try {
    const settings = PostStore.getQueueSettings();
    if (!settings.enabled) {
      return Response.json({ success: false, reason: "Queue paused" });
    }

    const posts = PostStore.getPosts();

    const queued = posts
      .filter((p: Post) => p.queuePosition !== undefined)
      .sort((a: Post, b: Post) => (a.queuePosition ?? 0) - (b.queuePosition ?? 0));

    if (queued.length === 0) {
      return Response.json({ success: false, reason: "Queue empty" });
    }

    const post = queued[0];

    // For now: Farcaster only
    if (post.networks.includes("farcaster")) {
      await postToFarcaster(post.content);
    }

    // Remove from queue + mark posted
    PostStore.updatePost(post.id, {
      status: "published",
      queuePosition: undefined,
      publishedAt: new Date(),
    });

    return Response.json({
      success: true,
      postedId: post.id,
    });
  } catch (err: any) {
    console.error("Queue run failed", err);
    return Response.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
