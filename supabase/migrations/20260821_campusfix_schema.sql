-- =============================================================
-- CampusFix AI — Supabase Native Database Schema & PL/pgSQL Functions
-- Project: bylhkgmwyncpsfokxjyr (VFSTR Campus)
-- =============================================================

-- 1. Create Tickets Table
CREATE TABLE IF NOT EXISTS campusfix_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_code VARCHAR(32) NOT NULL UNIQUE,
    user_id VARCHAR(128),
    role VARCHAR(64) DEFAULT 'Student',
    category VARCHAR(64) NOT NULL,
    location VARCHAR(255) NOT NULL,
    priority VARCHAR(32) DEFAULT 'NORMAL',
    status VARCHAR(32) DEFAULT 'ASSIGNED',
    issue_summary TEXT NOT NULL,
    assigned_team VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create Digital Twin Nodes Table
CREATE TABLE IF NOT EXISTS campusfix_digital_twin_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(64) NOT NULL UNIQUE,
    node_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    status VARCHAR(32) DEFAULT 'HEALTHY',
    packet_loss_pct NUMERIC(5,2) DEFAULT 0.00,
    latency_ms INT DEFAULT 12,
    jitter_ms NUMERIC(5,2) DEFAULT 1.20,
    rssi_dbm INT DEFAULT -48,
    active_users INT DEFAULT 0,
    mqtt_topic VARCHAR(255),
    last_ping TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create Users & SSO Accounts Table
CREATE TABLE IF NOT EXISTS campusfix_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(64) DEFAULT 'Student',
    department VARCHAR(255),
    primary_location VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Native PL/pgSQL Function: Auto Update Ticket Timestamp
CREATE OR REPLACE FUNCTION update_campusfix_ticket_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 5. Native Trigger: Auto Update Timestamp
DROP TRIGGER IF EXISTS trg_campusfix_tickets_updated AT ON campusfix_tickets;
CREATE TRIGGER trg_campusfix_tickets_updated
BEFORE UPDATE ON campusfix_tickets
FOR EACH ROW
EXECUTE FUNCTION update_campusfix_ticket_timestamp();
