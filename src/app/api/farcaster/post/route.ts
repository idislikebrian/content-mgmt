import { postToFarcaster } from "@/lib/farcaster";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { text } = body;

    if (!text || typeof text !== "string") {
      return Response.json(
        { success: false, error: "Missing text" },
        { status: 400 }
      );
    }

    const result = await postToFarcaster(text);

    return Response.json({
      success: true,
      result,
    });
  } catch (err: any) {
    console.error("Farcaster post failed:", err);
    return Response.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
