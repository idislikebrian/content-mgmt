export async function postToFarcasterClient(text: string) {
  const res = await fetch("/api/farcaster/post", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const json = await res.json();

  if (!json.success) {
    throw new Error(json.error || "Failed to post to Farcaster");
  }

  return json.result;
}