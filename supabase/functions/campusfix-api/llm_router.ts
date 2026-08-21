/**
 * CampusFix AI — VFSTR Multi-Complex Civic & IT Groq LLaMA-3.3-70B Engine (llm_router.ts)
 */

export class LlmRouter {
  private groqApiKey: string;

  constructor(apiKey?: string) {
    this.groqApiKey = apiKey || Deno.env.get("GROQ_API_KEY") || "";
  }

  isCasualOrUnrelatedQuery(query: string): 'greeting' | 'unrelated' | 'campus_it' {
    const q = (query || "").trim().toLowerCase();
    const clean = q.replace(/[^\w\s]/g, "");

    const greetings = ["hi", "hello", "hey", "hlo", "good morning", "good afternoon", "good evening", "namaste", "who are you", "how are you", "what is your name"];
    if (greetings.includes(clean) || clean.split(" ").every(w => ["hi", "hello", "hey", "there", "bot", "assistant"].includes(w))) {
      return 'greeting';
    }

    const unrelatedKeywords = [
      "weather", "joke", "cricket", "football", "ipl", "tokyo", "capital of", "recipe", "song", 
      "movie", "president", "prime minister", "who won", "2+2", "math", "poem"
    ];
    if (unrelatedKeywords.some(k => clean.includes(k)) && !clean.includes("wifi") && !clean.includes("vignan") && !clean.includes("portal") && !clean.includes("water") && !clean.includes("light") && !clean.includes("ac")) {
      return 'unrelated';
    }

    return 'campus_it';
  }

  async synthesizeDynamicResponse(
    role: string,
    location: string,
    category: string,
    userQuery: string,
    apNodeId: string,
    packetLoss: number,
    latency: number,
    ticketCode: string
  ): Promise<string | null> {
    if (!this.groqApiKey) return null;

    try {
      const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${this.groqApiKey}`
        },
        body: JSON.stringify({
          model: "llama-3.3-70b-versatile",
          messages: [
            {
              role: "system",
              content: `You are CollegeFix AI, the intelligent autonomous operations assistant for Vignan's Foundation for Science, Technology & Research (VFSTR), Vadlamudi.

You handle 6 Core Campus Civic & Infrastructure Complexes:
1. **IT_NET**: Wi-Fi Access Points (AP-HB-04, AP-CSE-01), SSO Portal Lockouts, Library Printer Jams, Smart Classroom AV.
2. **ELEC_HVAC**: AC Cooling Failures, Power Breaker Trips, Socket Repairs, Solar Hot Water Heaters, Campus High-Mast Lighting.
3. **PLUMB_SAN**: RO Water Purifiers, Restroom Flush Valves, Pipe Leaks, Rainwater Drainage.
4. **HYGIENE_CLEAN**: Mess Sanitation, Housekeeping & Dustbin Clearance, Sanitization.
5. **CIVIL_CARP**: Bench/Desk Repairs, Door Locks, Whiteboard Replacements, Elevator/Lift Sensor Maintenance.
6. **ESTATE_SEC**: CCTV Camera Alignment, Security Gate Scanners, Stray Animal Control, Campus Lighting Audits.

Always structure your answer cleanly using these EXACT markdown headers:
### 🔍 Step 1: Diagnostic Assessment
### 🛠️ Step 2: Telemetry & Work Order Check
### 📋 Step 3: Action Plan

Rules:
- Address the user's specific civic or IT issue directly in Step 1.
- Include live telemetry/work order references: Complex \`${category}\`, Work Order \`#${ticketCode}\` in Step 2.
- Provide 3 clear, actionable steps for resolution in Step 3.
- Keep the response concise, empathetic, and professional.`
            },
            {
              role: "user",
              content: `User Role: ${role}\nLocation: ${location}\nCivic Complex: ${category}\nWork Order Ref: #${ticketCode}\nUser Query: "${userQuery}"`
            }
          ],
          temperature: 0.65,
          max_tokens: 380
        })
      });

      if (resp.ok) {
        const data = await resp.json();
        const content = data.choices[0]?.message?.content;
        if (content && content.trim().length > 10) {
          return content.trim();
        }
      }
    } catch (err) {
      console.warn("Groq LLaMA-3.3 dynamic synthesis note:", err);
    }
    return null;
  }
}
