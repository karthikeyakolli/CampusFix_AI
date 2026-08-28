# CampusFix AI — Autonomous University IT Operations & Grievance Portal

**Live 100% Serverless Web Application** powered by **Supabase Cloud (Edge Functions + PostgreSQL PL/pgSQL RPCs)** for **Vignan's Foundation for Science, Technology & Research (VFSTR), Vadlamudi**.

---

## 🚀 Live GitHub Pages Deployment (Zero Local Server Required)

This repository is built for **100% online static deployment** via **GitHub Pages**. No local server or `localhost` setup is needed to run the application.

### 🌟 How to Enable GitHub Pages in 1 Click:
1. Go to your repository **Settings** on GitHub (`https://github.com/karthikeyakolli/CampusFix_AI/settings`).
2. Navigate to **Pages** in the left sidebar.
3. Under **Build and deployment** -> **Source**, select **Deploy from a branch**.
4. Set the branch to **`main`** and folder to **`/ (root)`**.
5. Click **Save**.

Your application is live at:
👉 **`https://karthikeyakolli.github.io/CampusFix_AI/`**

---

## 🧭 Multi-Role Portals & Modules

| Portal | URL Path | Description |
| :--- | :--- | :--- |
| **Grievance Studio** | [`index.html`](index.html) | Interactive student/faculty incident portal with satellite map, Vision AI, voice bot, and AI diagnostics. |
| **Institutional SSO** | [`login.html`](login.html) | Institutional Single Sign-On gateway with 1-click persona switching (Student, Faculty, Field Tech, Dean). |
| **Executive Command** | [`admin.html`](admin.html) | Central command dashboard with live thermal outage heatmaps, broadcast advisories, and ticket streams. |
| **NOC Operations** | [`it_admin.html`](it_admin.html) | Network Operations Center console monitoring live AP telemetry, jitter, packet loss, and incident clusters. |
| **Field Specialist** | [`worker.html`](worker.html) | Technician mobile workspace for GPS-guided ticket routing, step-by-step diagnostic workflows, and work order resolution. |

---

## 🏗️ Cloud Backend Architecture

### 1. Supabase Cloud Serverless Edge Function
- **Endpoint**: `https://bylhkgmwyncpsfokxjyr.supabase.co/functions/v1/campusfix-api`
- **Runtime**: Deno V8 TypeScript Native (Edge Functions v13)
- **Features**:
  - `GET /health` — Service health and telemetry status.
  - `GET /campus/layout` — VFSTR academic block and hostel registry.
  - `POST /chat` — Groq LLaMA-3.3-70B multi-complex civic classification & automated ticket persistence.
  - `GET /tickets` — Live ticket stream from Supabase PostgreSQL.
  - `POST /auth/login` — University SSO credential resolution.

### 2. Native PostgreSQL PL/pgSQL Stored Procedures & Triggers
- `fn_run_autonomous_agent` — Master autonomous orchestrator (perception, RAG retrieval, telemetry validation, ticket generation).
- `fn_spatial_temporal_correlation` — Automatically clusters multiple tickets in the same location into major incidents.
- `fn_authenticate_user` — User role and department resolution.
- `fn_check_telemetry_tool` — SNMP hardware diagnostic checks.
- `fn_rag_search` — Knowledge base procedure retrieval.

### 3. Standalone Python Backend (Optional Local Runner)
If you prefer running a local server:
```bash
# Start standalone Python server (port 8080)
python backend/server.py
```

---

## 📍 14 Aligned VFSTR Vadlamudi Campus Pinpoints

The system is calibrated with exact satellite GPS coordinates for:
1. **A-Block** (NTR Vignan Bhavan — Admin & Exam Cell)
2. **H-Block** (APJ Abdul Kalam — CSE, IT & AI)
3. **NTR Central Library** (L-Block — Digital Library & Resource Center)
4. **N-Block** (NLA Central Courtyard — Management & Law)
5. **Vignan Boys Hostel** (APJ Abdul Kalam Block B, Valmiki & Vasishta)
6. **P-Block** (School of Pharmaceutical Sciences)
7. **Vignan Main Ground** (Athletic Stadium)
8. **U-Block** (Aryabhatta — Mechanical & Civil)
9. **Convocation Hall** (Auditorium Arena)
10. **Lara New Block** (Emerging Technologies)
11. **Lara Block 1** (Main Academic Block 1)
12. **Lara Block 2** (Engineering Block 2)
13. **Guest House** (VIP Suites)
14. **Lara Playground** (East Sports Ground)

