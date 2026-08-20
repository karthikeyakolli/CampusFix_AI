-- ====================================================================
-- CampusFix — Production PostgreSQL / Supabase Schema (schema.sql)
-- Complete Architecture DDL: Tables, Vector Indexes, RBAC & RLS Security
-- ====================================================================

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector"; -- pgvector for RAG Knowledge Base Search

-- 2. USERS TABLE (RBAC)
CREATE TABLE IF NOT EXISTS campusfix_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Student' CHECK (role IN ('Student', 'Faculty', 'IT Staff', 'Admin')),
    department VARCHAR(100),
    primary_location VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. KNOWLEDGE BASE DOCUMENTS TABLE (RAG & pgvector)
CREATE TABLE IF NOT EXISTS campusfix_kb_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doc_code VARCHAR(50) UNIQUE NOT NULL, -- e.g. KB-WIFI-001, KB-LOGIN-001
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(768), -- Vector representation (Gemini text-embedding-004)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vector Search Index for RAG Queries
CREATE INDEX IF NOT EXISTS idx_campusfix_kb_embedding 
ON campusfix_kb_documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- 4. DIGITAL TWIN NODES TABLE (Campus Infrastructure)
CREATE TABLE IF NOT EXISTS campusfix_digital_twin_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_code VARCHAR(50) UNIQUE NOT NULL, -- e.g. AP-HB-04, PRN-LIB-01
    location VARCHAR(100) NOT NULL, -- e.g. Hostel B, Central Library
    service_name VARCHAR(100) NOT NULL, -- e.g. Campus Wi-Fi, Printing Gateway
    status VARCHAR(50) NOT NULL DEFAULT 'HEALTHY' CHECK (status IN ('HEALTHY', 'DEGRADED', 'OUTAGE', 'MAINTENANCE')),
    latency_ms INT DEFAULT 12,
    packet_loss_pct DECIMAL(5,2) DEFAULT 0.0,
    assigned_team VARCHAR(100) DEFAULT 'IT Helpdesk',
    last_checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. TICKETS TABLE
CREATE TABLE IF NOT EXISTS campusfix_tickets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_code VARCHAR(20) UNIQUE NOT NULL, -- e.g. CF-1042
    user_id UUID REFERENCES campusfix_users(id) ON DELETE SET NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Student',
    category VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    priority VARCHAR(50) NOT NULL DEFAULT 'MEDIUM' CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    status VARCHAR(50) NOT NULL DEFAULT 'NEW' CHECK (status IN ('NEW', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'ESCALATED', 'CLOSED')),
    issue_summary TEXT NOT NULL,
    evidence_data JSONB DEFAULT '{}'::jsonb,
    assigned_team VARCHAR(100) DEFAULT 'IT Helpdesk',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. INCIDENTS TABLE (Spatial-Temporal Correlation)
CREATE TABLE IF NOT EXISTS campusfix_incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_code VARCHAR(20) UNIQUE NOT NULL, -- e.g. INC-2026-001
    title VARCHAR(255) NOT NULL,
    location VARCHAR(100) NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    affected_user_count INT DEFAULT 1,
    correlation_score DECIMAL(4,3) NOT NULL DEFAULT 0.000,
    status VARCHAR(50) DEFAULT 'CANDIDATE',
    candidate_node_id UUID REFERENCES campusfix_digital_twin_nodes(id),
    assigned_team VARCHAR(100) DEFAULT 'Network Operations',
    evidence_cluster JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. AGENT AUDIT LOGS TABLE
CREATE TABLE IF NOT EXISTS campusfix_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    step_name VARCHAR(100) NOT NULL,
    confidence_score DECIMAL(4,3) NOT NULL DEFAULT 0.000,
    tool_name VARCHAR(100),
    tool_status VARCHAR(50),
    evidence_payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. SUPABASE ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE campusfix_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE campusfix_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE campusfix_audit_logs ENABLE ROW LEVEL SECURITY;

-- Indexes for Speed & Spatial Queries
CREATE INDEX IF NOT EXISTS idx_campusfix_tickets_loc ON campusfix_tickets (location, category);
CREATE INDEX IF NOT EXISTS idx_campusfix_incidents_loc ON campusfix_incidents (location, service_name);

-- SEED DATA
INSERT INTO campusfix_users (email, full_name, role, department, primary_location) VALUES
('alex.student@campus.edu', 'Alex Rivera', 'Student', 'Computer Science', 'Hostel B'),
('dr.smith@campus.edu', 'Dr. Sarah Smith', 'Faculty', 'Electrical Engineering', 'Academic Building A'),
('it.admin@campus.edu', 'Marcus Vance', 'IT Staff', 'Network Operations', 'Administration Block')
ON CONFLICT (email) DO NOTHING;

INSERT INTO campusfix_digital_twin_nodes (node_code, location, service_name, status, latency_ms, packet_loss_pct, assigned_team) VALUES
('AP-HB-04', 'Hostel B', 'Campus Wi-Fi', 'DEGRADED', 340, 82.50, 'Network Operations'),
('GW-ACAD-01', 'Academic Building A', 'Student Portal Gateway', 'HEALTHY', 14, 0.00, 'IT Helpdesk'),
('PRN-LIB-01', 'Central Library', 'Networked Printing System', 'HEALTHY', 18, 0.00, 'IT Helpdesk'),
('SW-ADMIN-02', 'Administration Block', 'Staff Ethernet Network', 'HEALTHY', 8, 0.00, 'Infrastructure Team')
ON CONFLICT (node_code) DO NOTHING;

INSERT INTO campusfix_kb_documents (doc_code, title, category, content, metadata) VALUES
('KB-WIFI-001', 'Campus Wi-Fi Connectivity & AP Troubleshooting', 'wifi', 'Symptoms: campus Wi-Fi authentication or packet degradation. Safe diagnostic steps: verify SSID, check account state, ping location AP node. Verify access to campus portal. Escalate if multiple users or AP degraded.', '{"tags": ["wifi", "network", "ap"]}'::jsonb),
('KB-LOGIN-001', 'Student Portal SSO Authentication Protocol', 'login', 'Security requirement: Never request user passwords. Verify account active state in directory tool. Guide approved SSO self-service password reset. Verify successful portal login. Escalate if active account still cannot authenticate.', '{"tags": ["login", "sso", "security"]}'::jsonb),
('KB-PRINTER-001', 'Library & Lab Print Server Hardware Protocol', 'printer', 'Query printer ID and physical location. Execute safe queue status diagnostic tool. Guide standard paper jam / toner check. If hardware fault or spooler crash persists, generate ticket CF for IT Helpdesk hardware dispatch.', '{"tags": ["printer", "hardware"]}'::jsonb)
ON CONFLICT (doc_code) DO NOTHING;

INSERT INTO campusfix_tickets (ticket_code, category, location, priority, status, issue_summary, assigned_team) VALUES
('CF-1042', 'wifi', 'Hostel B', 'HIGH', 'ASSIGNED', 'Wi-Fi access point AP-HB-04 high packet loss reported by multiple students in Hostel B', 'Network Operations'),
('CF-1041', 'login', 'Academic Building A', 'MEDIUM', 'RESOLVED', 'Student SSO portal authentication reset completed', 'IT Helpdesk'),
('CF-1039', 'printer', 'Central Library', 'LOW', 'ESCALATED', 'Printer PRN-LIB-01 paper jam hardware error', 'IT Helpdesk')
ON CONFLICT (ticket_code) DO NOTHING;
