/**
 * CampusFix AI — Deepgram Voice Service Client (deepgram.ts)
 * Converted from Python deepgram_service.py.
 */

export class DeepgramVoiceService {
  private apiKey: string;

  constructor(apiKey?: string) {
    this.apiKey = apiKey || Deno.env.get("DEEPGRAM_API_KEY") || "";
  }

  /**
   * Generates high-fidelity MP3 voice audio using Deepgram Aura TTS API.
   * Returns base64 encoded audio string for web player streaming.
   */
  async generateTtsAudio(text: string, model: string = "aura-asteria-en", language: string = "en"): Promise<{ audio_base64: string | null; error?: string }> {
    if (!this.apiKey) {
      return { audio_base64: null, error: "Deepgram API key not configured" };
    }

    if (language === "te") model = "aura-luna-en";
    else if (language === "hi") model = "aura-asteria-en";

    const url = `https://api.deepgram.com/v1/speak?model=${model}`;

    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: {
          "Authorization": `Token ${this.apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
      });

      if (resp.ok) {
        const buffer = await resp.arrayBuffer();
        const base64Audio = btoa(String.fromCharCode(...new Uint8Array(buffer)));
        return { audio_base64: base64Audio };
      }
    } catch (err) {
      console.warn("Deepgram TTS error:", err);
    }

    return { audio_base64: null, error: "TTS generation failed" };
  }
}
