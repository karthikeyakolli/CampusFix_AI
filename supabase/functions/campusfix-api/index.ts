import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { AgentGraphEngine } from "./agent_graph.ts";
import { DeepgramVoiceService } from "./deepgram.ts";
import { InfrastructureTools } from "./tools.ts";
import { ChatRequest } from "./types.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS, PUT, DELETE",
};

const agentEngine = new AgentGraphEngine();
const voiceService = new DeepgramVoiceService();

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  const url = new URL(req.url);
  const path = url.pathname;

  const SUPABASE_URL = Deno.env.get("SUPABASE_URL") || "https://bylhkgmwyncpsfokxjyr.supabase.co";
  const SUPABASE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || Deno.env.get("SUPABASE_ANON_KEY") || "";

  try {
    // 1. Health Check Endpoint
    if (path.endsWith("/health") || path.endsWith("/campusfix-api")) {
      if (req.method === "GET") {
        return new Response(
          JSON.stringify({
            ok: true,
            service: "CampusFix Autonomous Edge Backend",
            runtime: "Supabase Edge Functions (Deno V8 TypeScript Native)",
            version: "7.0.0",
            project_id: "bylhkgmwyncpsfokxjyr",
            vfstr_layout_registry: true
          }),
          { headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }
    }

    // 2. VFSTR Campus Building & Hostel Registry Endpoint
    if (path.endsWith("/campus/layout") && req.method === "GET") {
      return new Response(
        JSON.stringify({
          university_name: "Vignan's Foundation for Science, Technology & Research (VFSTR), Vadlamudi",
          academic_blocks: InfrastructureTools.vfstrBlocks,
          hostel_complexes: InfrastructureTools.vfstrHostels
        }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 3. Auth SSO Login Endpoint
    if (path.endsWith("/auth/login") && req.method === "POST") {
      let payload: any = {};
      try { payload = await req.json(); } catch (_e) {}
      const identifier = (payload.identifier || "").trim().toLowerCase();
      
      let role = "Student";
      let dept = "Computer Science";
      let loc = "Hostel B";

      if (identifier.includes("dr.") || identifier.includes("faculty") || identifier.includes("smith")) {
        role = "Faculty";
        dept = "CSE Faculty Dept (H-Block)";
        loc = "H-Block CSE";
      } else if (identifier.includes("admin") || identifier.includes("staff") || identifier.includes("vance")) {
        role = "IT Staff";
        dept = "Network Operations";
        loc = "A-Block Admin";
      }

      const name = identifier.split("@")[0].replace(".", " ").replace(/\b\w/g, l => l.toUpperCase()) || "Student User";
      return new Response(JSON.stringify({
        authenticated: true,
        email: identifier.includes("@") ? identifier : `${identifier}@vignan.ac.in`,
        full_name: name,
        role: role,
        department: dept,
        primary_location: loc
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
    }

    // 4. Deepgram Voice TTS Endpoint
    if (path.endsWith("/voice/tts") && req.method === "POST") {
      let body: any = {};
      try { body = await req.json(); } catch (_e) {}
      const result = await voiceService.generateTtsAudio(body.text || "Hello", body.model || "aura-asteria-en", body.language || "en");
      return new Response(JSON.stringify(result), {
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }

    // 5. GET /tickets Endpoint
    if (path.endsWith("/tickets")) {
      if (req.method === "GET") {
        try {
          const resp = await fetch(`${SUPABASE_URL}/rest/v1/campusfix_tickets?select=*&order=created_at.desc`, {
            headers: { "apikey": SUPABASE_KEY, "Authorization": `Bearer ${SUPABASE_KEY}` }
          });
          if (resp.ok) {
            const tickets = await resp.json();
            return new Response(JSON.stringify(tickets), {
              headers: { ...corsHeaders, "Content-Type": "application/json" }
            });
          }
        } catch (err) {
          console.warn("Fetch tickets error:", err);
        }
      }
    }

    // 6. Sub-Second Autonomous Chat Engine Endpoint
    if (path.endsWith("/chat") || path.endsWith("/api/chat") || req.method === "POST") {
      let body: ChatRequest = { message: "Wi-Fi query" };
      try {
        body = await req.json();
      } catch (_e) {
        // Fallback default
      }

      // Execute Autonomous Agent Engine
      const chatResponse = await agentEngine.processRequest(body);

      // Auto-persist ticket record into Supabase PostgreSQL table if IT ticket generated
      if (chatResponse.assigned_ticket) {
        try {
          await fetch(`${SUPABASE_URL}/rest/v1/campusfix_tickets`, {
            method: "POST",
            headers: {
              "apikey": SUPABASE_KEY,
              "Authorization": `Bearer ${SUPABASE_KEY}`,
              "Content-Type": "application/json",
              "Prefer": "return=minimal"
            },
            body: JSON.stringify({
              ticket_code: chatResponse.assigned_ticket.ticket_code,
              category: chatResponse.assigned_ticket.category.toLowerCase(),
              location: chatResponse.assigned_ticket.location,
              issue_summary: body.message || "Campus IT Request",
              priority: chatResponse.assigned_ticket.priority,
              role: body.role || "Student",
              assigned_team: chatResponse.assigned_ticket.department,
              status: "ASSIGNED"
            })
          });
        } catch (err) {
          console.warn("Supabase edge db insert note:", err);
        }
      }

      return new Response(JSON.stringify(chatResponse), {
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }

    return new Response(JSON.stringify({ error: "Endpoint Not Found" }), {
      status: 404,
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: String(error) }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  }
});
