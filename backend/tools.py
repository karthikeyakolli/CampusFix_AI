"""
CampusFix AI — Safe Tool Adapters & Resilience Module (tools.py)
Implements read-only diagnostic checks and tool failure recovery logic.
"""

from typing import Dict, Any, Tuple
import random

class SafeToolAdapter:
    """Safe read-only infrastructure tools with fault injection recovery."""
    
    @staticmethod
    def check_ap_status(location: str, inject_failure: bool = False) -> Tuple[bool, Dict[str, Any]]:
        """
        Check Access Point ping, packet loss, and latency for a given campus location.
        Returns: (success: bool, telemetry: Dict[str, Any])
        """
        if inject_failure:
            # Tool failure simulation (Scenario SCN-003)
            return False, {
                "error": "504 Gateway Timeout — Network AP SNMP Agent Unresponsive",
                "tool_name": "check_ap_status",
                "recovery_strategy": "Fall back to secondary KB evidence & historical incident log"
            }
        
        loc_lower = location.lower() if location else ""
        if "hostel" in loc_lower or "hostel b" in loc_lower:
            return True, {
                "ap_id": "AP-HB-04",
                "location": "Hostel B (Vignan Boys Hostel)",
                "status": "DEGRADED",
                "packet_loss_pct": 82.5,
                "latency_ms": 340,
                "jitter_ms": 48.2,
                "rssi_dbm": -84,
                "bandwidth_mbps": 1.2,
                "connected_clients": 142,
                "mqtt_topic": "vfstr/telemetry/hostel_b/ap_hb_04",
                "detail": "High 2.4GHz/5GHz co-channel interference & 82.5% packet loss on AP-HB-04"
            }
        elif "cse" in loc_lower or "h-block" in loc_lower:
            return True, {
                "ap_id": "AP-HBLOCK-CSE-01",
                "location": "H-Block (CSE Department)",
                "status": "HEALTHY",
                "packet_loss_pct": 0.0,
                "latency_ms": 12,
                "jitter_ms": 1.4,
                "rssi_dbm": -42,
                "bandwidth_mbps": 850.0,
                "connected_clients": 86,
                "mqtt_topic": "vfstr/telemetry/hblock/ap_cse_01",
                "detail": "HPC Fiber Backhaul operational at 1Gbps"
            }
        elif "library" in loc_lower:
            return True, {
                "ap_id": "AP-LIB-01",
                "location": "Central Library (L-Block)",
                "status": "HEALTHY",
                "packet_loss_pct": 0.2,
                "latency_ms": 14,
                "jitter_ms": 2.1,
                "rssi_dbm": -55,
                "bandwidth_mbps": 450.0,
                "connected_clients": 68,
                "mqtt_topic": "vfstr/telemetry/library/ap_lib_01",
                "detail": "All AP nodes in Central Library operating normally"
            }
        else:
            return True, {
                "ap_id": "AP-GENERIC-01",
                "location": location or "Campus Main",
                "status": "HEALTHY",
                "packet_loss_pct": 0.0,
                "latency_ms": 12,
                "jitter_ms": 1.2,
                "rssi_dbm": -48,
                "bandwidth_mbps": 500.0,
                "connected_clients": 45,
                "mqtt_topic": "vfstr/telemetry/main/ap_01",
                "detail": "SNMP Telemetry Socket healthy"
            }

    @staticmethod
    def check_account_status(user_email: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Safely check Directory Account active state.
        Zero password risk constraint: Never requests or stores passwords.
        """
        return True, {
            "account": user_email,
            "status": "ACTIVE",
            "sso_bound": True,
            "mfa_enabled": True,
            "password_expired": False,
            "security_note": "Password is never requested or logged by CampusFix AI"
        }

    @staticmethod
    def check_printer_queue(printer_id: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Check printer hardware queue and error sensors.
        """
        if "lib" in printer_id.lower() or "library" in printer_id.lower():
            return True, {
                "printer_id": "PRN-LIB-01",
                "location": "Central Library",
                "online": True,
                "paper_tray": "JAMMED",
                "toner_level_pct": 74,
                "queued_jobs": 8,
                "error_sensor": "HARDWARE_PAPER_FEED_JAM"
            }
        return True, {
            "printer_id": printer_id or "PRN-GENERIC-01",
            "location": "Academic Building A",
            "online": True,
            "paper_tray": "OK",
            "toner_level_pct": 92,
            "queued_jobs": 1,
            "error_sensor": "NONE"
        }
