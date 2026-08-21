/**
 * CampusFix AI — Supabase Native TypeScript Data Models (types.ts)
 * Converted from Python models.py & Pydantic schemas.
 */

export interface ChatRequest {
  message: string;
  role?: 'Student' | 'Faculty' | 'IT Staff' | string;
  location?: string;
  user_email?: string;
}

export interface AssignedTicket {
  ticket_code: string;
  problem_summary: string;
  assigned_to: string;
  department: string;
  location: string;
  category: string;
  priority: 'EMERGENCY' | 'HIGH' | 'NORMAL' | 'LOW';
  status: 'NEW' | 'ASSIGNED' | 'IN_PROGRESS' | 'RESOLVED';
  estimated_resolution: string;
}

export interface TimelineEvent {
  step_name: string;
  title: string;
  detail: string;
}

export interface ChatResponse {
  message: string;
  category: string;
  confidence: number;
  location: string;
  ticket_id: string;
  assigned_ticket: AssignedTicket;
  evidence_list: string[];
  timeline_events: TimelineEvent[];
  simulated: boolean;
}

export interface ApTelemetryNode {
  ap_id: string;
  location: string;
  status: 'HEALTHY' | 'DEGRADED' | 'OFFLINE';
  packet_loss_pct: number;
  latency_ms: number;
  jitter_ms: number;
  rssi_dbm: number;
  bandwidth_mbps: number;
  connected_clients: number;
  mqtt_topic: string;
  detail: string;
}

export interface UserSession {
  authenticated: boolean;
  email: string;
  full_name: string;
  role: string;
  department: string;
  primary_location: string;
}
