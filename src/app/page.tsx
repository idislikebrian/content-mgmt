"use client";

import { useState, useEffect } from "react";
import { PostComposer } from "@/components/post-composer";
import { PostLibrary } from "@/components/post-library";
import { CalendarView } from "@/components/calendar-view";
import { ScheduleDialog } from "@/components/schedule-dialog";
import { QueueManager } from "@/components/queue-manager";
import { NetworkSettings } from "@/components/network-settings";
import { AnalyticsDashboard } from "@/components/analytics-dashboard";
import { usePosts } from "@/hooks/use-posts";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FileText, Calendar, Repeat, BarChart3, Settings } from "lucide-react";
import type { Post, NetworkType } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { generateDemoAnalytics } from "@/lib/demo-data";
import { PostStore } from "@/lib/store";
import { postToFarcasterClient } from "@/lib/post-to-network";

import styles from "./page.module.css";

export default function Home() {
  const { posts, addPost, deletePost, updatePost, enqueuePost } = usePosts();

  const [activeTab, setActiveTab] = useState("library");
  const [scheduleDialogOpen, setScheduleDialogOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date>();
  const [selectedPost, setSelectedPost] = useState<Post>();
  const [showSettings, setShowSettings] = useState(false);
  const [allPosts, setAllPosts] = useState<Post[]>(posts);

  useEffect(() => {
    const existingPosts = PostStore.getPosts();
    if (existingPosts.length === 0) {
      const demoData = generateDemoAnalytics();
      PostStore.savePosts(demoData);
      setAllPosts(demoData);
    } else {
      setAllPosts(existingPosts);
    }
  }, []);

  useEffect(() => {
    setAllPosts(posts);
  }, [posts]);

  const handleScheduleFromCalendar = (
    content: string,
    networks: NetworkType[],
    scheduledFor: Date
  ) => {
    if (selectedPost) {
      updatePost(selectedPost.id, {
        content,
        networks,
        scheduledFor,
        status: "scheduled",
      });
    } else {
      addPost(content, networks, scheduledFor);
    }

    setSelectedPost(undefined);
    setSelectedDate(undefined);
  };

  return (
    <div className={styles.page}>
      <header>
        <div className={styles.nav}>
          <h1>content mgmt</h1>
        </div>
        <Button
          variant="outline"
          onClick={() => setShowSettings(!showSettings)}
        >
          <Settings />
          {showSettings ? "Hide Settings" : "Network Settings"}
        </Button>
      </header>

      <main className={styles.main}>
        {showSettings ? (
          <NetworkSettings />
        ) : (
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList>
              <TabsTrigger value="library">
                <FileText />
                Library
              </TabsTrigger>
              <TabsTrigger value="calendar">
                <Calendar />
                Calendar
              </TabsTrigger>
              <TabsTrigger value="queue">
                <Repeat />
                Queue
              </TabsTrigger>
              <TabsTrigger value="analytics">
                <BarChart3 />
                Analytics
              </TabsTrigger>
            </TabsList>

            <TabsContent value="library">
              <PostComposer
                onSave={(content, networks, scheduledFor) => {
                  addPost(content, networks, scheduledFor);
                }}
                onPostNow={async (content, networks) => {
                  if (networks.includes("farcaster")) {
                    await postToFarcasterClient(content);
                  }
                }}
                onAddToQueue={(content, networks) => {
                  const post = addPost(content, networks);
                  enqueuePost(post.id);
                  setActiveTab("queue");
                }}
              />

              <div>
                <h2>Your Posts</h2>
                <PostLibrary
                  posts={allPosts}
                  onDelete={deletePost}
                  onEdit={(post) => {
                    setSelectedPost(post);
                    setScheduleDialogOpen(true);
                  }}
                  onSchedule={(post) => {
                    setSelectedPost(post);
                    setScheduleDialogOpen(true);
                  }}
                />
              </div>
            </TabsContent>

            <TabsContent value="calendar">
              <CalendarView
                posts={allPosts}
                onDayClick={(date) => {
                  setSelectedDate(date);
                  setSelectedPost(undefined);
                  setScheduleDialogOpen(true);
                }}
                onPostClick={(post) => {
                  setSelectedPost(post);
                  setSelectedDate(post.scheduledFor);
                  setScheduleDialogOpen(true);
                }}
              />
            </TabsContent>

            <TabsContent value="queue">
              <QueueManager
                posts={allPosts}
                onUpdatePost={updatePost}
              />
            </TabsContent>

            <TabsContent value="analytics">
              <AnalyticsDashboard posts={allPosts} />
            </TabsContent>
          </Tabs>
        )}
      </main>

      <ScheduleDialog
        open={scheduleDialogOpen}
        onOpenChange={setScheduleDialogOpen}
        selectedDate={selectedDate}
        post={selectedPost}
        onSchedule={handleScheduleFromCalendar}
      />
    </div>
  );
}
