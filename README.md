# CampusFix AI — Autonomous University IT Operations & Grievance Portal

**Live 100% Serverless Web Application** powered by **Supabase Cloud (Edge Functions + PostgreSQL PL/pgSQL RPCs)**.

---

## 🚀 Live GitHub Pages Deployment (Zero Local Server Required)

This repository is built for **100% online static deployment** via **GitHub Pages**. No local Python server or `localhost` setup is needed to run the application.

### 🌟 How to Enable GitHub Pages in 1 Click:
1. Go to your repository **Settings** on GitHub (`https://github.com/karthikeyakolli/CampusFix_AI/settings`).
2. Navigate to **Pages** in the left sidebar.
3. Under **Build and deployment** -> **Source**, select **Deploy from a branch**.
4. Set the branch to **`main`** and folder to **`/ (root)`**.
5. Click **Save**.

Your application will be live at:
👉 **`https://karthikeyakolli.github.io/CampusFix_AI/`**

---

## 🏗️ Architecture & Features
- **100% Serverless**: Connects directly to live Supabase Cloud Edge Functions (`/functions/v1/campusfix-api`) and REST API RPC procedures (`fn_run_autonomous_agent`).
- **Offline & Standalone Fallback**: Includes built-in client-side Cognitive AI engine for instant offline execution.
- **VFSTR Vadlamudi Campus Recognition**: Tailored for Blocks A, N, H, P, U, Hostel B, Priyadarshini Hostel, and Central Library.
- **Multi-Lingual Voice Bot**: Full-duplex speech recognition in **English**, **Telugu (తెలుగు)**, and **Hindi (हिंदी)**.
- **NOC Admin Console**: Integrated IT Operations dashboard (`it_admin.html`) with real-time ticket stream and telemetry matrix.
