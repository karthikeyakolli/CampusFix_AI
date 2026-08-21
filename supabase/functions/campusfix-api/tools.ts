/**
 * CampusFix AI — VFSTR Campus Knowledge Base & Telemetry Engine (tools.ts)
 * Trained for Vignan's Foundation for Science, Technology & Research (VFSTR), Vadlamudi.
 */

export interface VfstrBuildingBlock {
  block_code: string;
  official_name: string;
  department: string;
  total_floors: number;
  total_rooms: number;
  floors_detail: { floor_number: number; floor_name: string; room_range: string; key_facilities: string[] }[];
}

export interface VfstrHostelBuilding {
  hostel_code: string;
  hostel_name: string;
  gender: 'Boys' | 'Girls' | 'International';
  total_floors: number;
  total_rooms: number;
  capacity: number;
  room_types: string[];
  ap_nodes: string[];
}

export class InfrastructureTools {
  // VFSTR Academic & Administrative Blocks Knowledge Data (Used by AI Model for Training)
  static vfstrBlocks: VfstrBuildingBlock[] = [
    {
      block_code: "A-BLOCK",
      official_name: "NTR Vignan Bhavan (Administrative Block)",
      department: "University Administration, VC Office, Registrar, T&P Cell, Finance",
      total_floors: 5,
      total_rooms: 85,
      floors_detail: [
        { floor_number: 0, floor_name: "Ground Floor", room_range: "A-001 to A-018", key_facilities: ["Reception", "Admission Cell", "Registrar Office", "Finance Office"] },
        { floor_number: 1, floor_name: "1st Floor", room_range: "A-101 to A-118", key_facilities: ["Vice-Chancellor Office", "Dean Academics Desk", "IQAC Cell"] },
        { floor_number: 2, floor_name: "2nd Floor", room_range: "A-201 to A-220", key_facilities: ["Training & Placement (T&P) Cell", "Corporate Interview Rooms"] },
        { floor_number: 3, floor_name: "3rd Floor", room_range: "A-301 to A-318", key_facilities: ["Controller of Examinations (CoE)", "Evaluation Halls"] },
        { floor_number: 4, floor_name: "4th Floor", room_range: "A-401 to A-415", key_facilities: ["Sangam Seminar Hall", "Spoorthy Boardroom", "Executive Lounge"] }
      ]
    },
    {
      block_code: "H-BLOCK",
      official_name: "Homi Bhabha Block (CSE & ECE Academic Complex)",
      department: "Computer Science & Engineering (CSE), Electronics & Communication (ECE)",
      total_floors: 6,
      total_rooms: 130,
      floors_detail: [
        { floor_number: 0, floor_name: "Ground Floor", room_range: "H-001 to H-022", key_facilities: ["Advanced AI Center of Excellence", "GPU Server Room", "HOD CSE Office"] },
        { floor_number: 1, floor_name: "1st Floor", room_range: "H-101 to H-124", key_facilities: ["Smart Classrooms H-101 to H-110", "Computer Networks Lab"] },
        { floor_number: 2, floor_name: "2nd Floor", room_range: "H-201 to H-224", key_facilities: ["Software Engineering Lab", "Full-Stack Dev Lab", "Data Structures Lab"] },
        { floor_number: 3, floor_name: "3rd Floor", room_range: "H-301 to H-322", key_facilities: ["ECE Signal Processing Lab", "VLSI Design Center", "HOD ECE Office"] },
        { floor_number: 4, floor_name: "4th Floor", room_range: "H-401 to H-422", key_facilities: ["Embedded Systems & IoT Lab", "Robotics Hardware Testing"] },
        { floor_number: 5, floor_name: "5th Floor", room_range: "H-501 to H-518", key_facilities: ["Cyber Security Lab", "Cloud Computing Center", "Seminar Hall H-501"] }
      ]
    },
    {
      block_code: "N-BLOCK",
      official_name: "NLA Block (School of Management, Law & Humanities)",
      department: "MBA / BBA Management Studies, School of Law, English & Humanities",
      total_floors: 6,
      total_rooms: 120,
      floors_detail: [
        { floor_number: 0, floor_name: "Ground Floor", room_range: "N-001 to N-020", key_facilities: ["Moot Court Hall", "Law Library Desk", "Dean Law Office"] },
        { floor_number: 1, floor_name: "1st Floor", room_range: "N-101 to N-120", key_facilities: ["MBA Smart Lecture Halls N-101 to N-110", "Case Study Discussion Rooms"] },
        { floor_number: 2, floor_name: "2nd Floor", room_range: "N-201 to N-220", key_facilities: ["Financial Analytics Lab", "HOD Management Office"] },
        { floor_number: 3, floor_name: "3rd Floor", room_range: "N-301 to N-320", key_facilities: ["BBA Classrooms N-301 to N-315", "English Communication Skill Lab"] },
        { floor_number: 4, floor_name: "4th Floor", room_range: "N-401 to N-420", key_facilities: ["Law Classrooms N-401 to N-415", "Legal Aid Cell"] },
        { floor_number: 5, floor_name: "5th Floor", room_range: "N-501 to N-520", key_facilities: ["N-Block Executive Auditorium", "Humanities Research Center"] }
      ]
    },
    {
      block_code: "U-BLOCK",
      official_name: "Aryabhatta Block (Mechanical & Civil Complex)",
      department: "Mechanical Engineering, Civil Engineering, Mechatronics",
      total_floors: 5,
      total_rooms: 95,
      floors_detail: [
        { floor_number: 0, floor_name: "Ground Floor", room_range: "U-001 to U-018", key_facilities: ["Heavy Machines Workshop", "Strength of Materials Lab", "CNC Machining"] },
        { floor_number: 1, floor_name: "1st Floor", room_range: "U-101 to U-120", key_facilities: ["CAD/CAM Lab", "Thermal Engineering Lab", "HOD Mechanical"] },
        { floor_number: 2, floor_name: "2nd Floor", room_range: "U-201 to U-220", key_facilities: ["Fluid Mechanics Lab", "Surveying Lab", "HOD Civil"] },
        { floor_number: 3, floor_name: "3rd Floor", room_range: "U-301 to U-320", key_facilities: ["Structural Engineering Lab", "Environmental Testing Lab"] },
        { floor_number: 4, floor_name: "4th Floor", room_range: "U-401 to U-417", key_facilities: ["Robotics & Automation Hub", "CAD Simulation Center"] }
      ]
    },
    {
      block_code: "L-BLOCK",
      official_name: "Vignan NTR Central Library Block",
      department: "Central Digital Library, Learning Resource Center, EZProxy Hub",
      total_floors: 4,
      total_rooms: 42,
      floors_detail: [
        { floor_number: 0, floor_name: "Ground Floor", room_range: "L-001 to L-010", key_facilities: ["Digital Circulation Desk", "PRN-LIB-01 Printing Kiosk", "Book Stacks"] },
        { floor_number: 1, floor_name: "1st Floor", room_range: "L-101 to L-112", key_facilities: ["IEEE & Springer Digital Resource Center", "PRN-LIB-02 Backup Kiosk"] },
        { floor_number: 2, floor_name: "2nd Floor", room_range: "L-201 to L-210", key_facilities: ["Research Scholar Reading Room", "Journal Archives"] },
        { floor_number: 3, floor_name: "3rd Floor", room_range: "L-301 to L-310", key_facilities: ["Group Discussion Cabins", "Quiet Study Zone"] }
      ]
    },
    {
      block_code: "PHARM-BLOCK",
      official_name: "School of Pharmaceutical Sciences Block",
      department: "Pharmacy, Pharmaceutical Chemistry, Pharmacology",
      total_floors: 4,
      total_rooms: 55,
      floors_detail: [
        { floor_number: 0, floor_name: "Ground Floor", room_range: "P-001 to P-014", key_facilities: ["Pharmaceutics Lab", "Medicinal Chemistry Lab"] },
        { floor_number: 1, floor_name: "1st Floor", room_range: "P-101 to P-114", key_facilities: ["Pharmacology Testing Lab", "Analysis Instrument Room"] },
        { floor_number: 2, floor_name: "2nd Floor", room_range: "P-201 to P-214", key_facilities: ["Pharmacognosy Research Lab", "Dean Pharmacy Desk"] },
        { floor_number: 3, floor_name: "3rd Floor", room_range: "P-301 to P-313", key_facilities: ["Herbal Drug Development", "Pharmacy Seminar Hall"] }
      ]
    }
  ];

  // VFSTR Hostels Knowledge Data
  static vfstrHostels: VfstrHostelBuilding[] = [
    {
      hostel_code: "VB-HOSTEL-A",
      hostel_name: "Visweswaraya Boys Hostel (Block A)",
      gender: "Boys",
      total_floors: 5,
      total_rooms: 200,
      capacity: 800,
      room_types: ["4-Occupancy Non-AC", "2-Occupancy Deluxe AC"],
      ap_nodes: ["AP-HA-01", "AP-HA-02", "AP-HA-03"]
    },
    {
      hostel_code: "VB-HOSTEL-B",
      hostel_name: "APJ Abdul Kalam Boys Hostel (Block B)",
      gender: "Boys",
      total_floors: 5,
      total_rooms: 225,
      capacity: 900,
      room_types: ["4-Occupancy Non-AC", "4-Occupancy AC", "2-Occupancy Deluxe AC"],
      ap_nodes: ["AP-HB-01", "AP-HB-02", "AP-HB-03", "AP-HB-04 (Hostel B Corridor)"]
    },
    {
      hostel_code: "VB-HOSTEL-C",
      hostel_name: "C.V. Raman Boys Hostel (Block C)",
      gender: "Boys",
      total_floors: 4,
      total_rooms: 140,
      capacity: 560,
      room_types: ["4-Occupancy Non-AC"],
      ap_nodes: ["AP-HC-01", "AP-HC-02"]
    },
    {
      hostel_code: "PG-HOSTEL-1",
      hostel_name: "Priyadarshini Girls Hostel (Sarojini Naidu Block 1)",
      gender: "Girls",
      total_floors: 5,
      total_rooms: 250,
      capacity: 1000,
      room_types: ["4-Occupancy Non-AC", "3-Occupancy AC", "Attached Bath AC"],
      ap_nodes: ["AP-PG1-01", "AP-PG1-02", "AP-PG1-03"]
    },
    {
      hostel_code: "PG-HOSTEL-2",
      hostel_name: "Priyadarshini Girls Hostel (Kalpana Chawla Block 2)",
      gender: "Girls",
      total_floors: 5,
      total_rooms: 250,
      capacity: 1000,
      room_types: ["4-Occupancy Non-AC", "3-Occupancy AC"],
      ap_nodes: ["AP-PG2-01", "AP-PG2-02", "AP-PG2-03"]
    },
    {
      hostel_code: "INT-HOSTEL",
      hostel_name: "VFSTR International Scholars Residence",
      gender: "International",
      total_floors: 4,
      total_rooms: 80,
      capacity: 160,
      room_types: ["Single Suite AC", "2-Occupancy Suite AC"],
      ap_nodes: ["AP-INT-01", "AP-INT-02"]
    }
  ];

  static checkApStatus(location: string) {
    const locLower = (location || "").toLowerCase();

    if (locLower.includes("hostel b") || locLower.includes("abdul kalam") || locLower.includes("hb-04")) {
      return {
        ap_id: "AP-HB-04",
        location: "APJ Abdul Kalam Boys Hostel (Block B, 2nd Floor Corridor)",
        status: "DEGRADED" as const,
        packet_loss_pct: 82.5,
        latency_ms: 340,
        jitter_ms: 48.2,
        rssi_dbm: -84,
        bandwidth_mbps: 1.2,
        connected_clients: 142,
        mqtt_topic: "vfstr/telemetry/hostel_b/ap_hb_04",
        detail: "High 2.4GHz/5GHz co-channel interference & 82.5% packet loss on AP-HB-04"
      };
    } else if (locLower.includes("n-block") || locLower.includes("nla") || locLower.includes("law") || locLower.includes("management")) {
      return {
        ap_id: "AP-NBLOCK-01",
        location: "N-Block (Management & Law Block, 6 Floors, 20 Rooms/Floor)",
        status: "HEALTHY" as const,
        packet_loss_pct: 0.1,
        latency_ms: 15,
        jitter_ms: 1.8,
        rssi_dbm: -48,
        bandwidth_mbps: 600.0,
        connected_clients: 94,
        mqtt_topic: "vfstr/telemetry/nblock/ap_n_01",
        detail: "N-Block Wi-Fi operational across all 6 floors and 120 rooms"
      };
    } else if (locLower.includes("cse") || locLower.includes("h-block") || locLower.includes("homi bhabha")) {
      return {
        ap_id: "AP-HBLOCK-CSE-01",
        location: "Homi Bhabha Block (H-Block 1st Floor CSE Labs)",
        status: "HEALTHY" as const,
        packet_loss_pct: 0.0,
        latency_ms: 12,
        jitter_ms: 1.4,
        rssi_dbm: -42,
        bandwidth_mbps: 850.0,
        connected_clients: 86,
        mqtt_topic: "vfstr/telemetry/hblock/ap_cse_01",
        detail: "HPC Fiber Backhaul operational at 1Gbps"
      };
    } else if (locLower.includes("library") || locLower.includes("l-block") || locLower.includes("central library")) {
      return {
        ap_id: "AP-LIB-01",
        location: "Vignan NTR Central Library (L-Block Ground Floor)",
        status: "HEALTHY" as const,
        packet_loss_pct: 0.2,
        latency_ms: 14,
        jitter_ms: 2.1,
        rssi_dbm: -55,
        bandwidth_mbps: 450.0,
        connected_clients: 68,
        mqtt_topic: "vfstr/telemetry/library/ap_lib_01",
        detail: "All AP nodes in Central Library operating normally"
      };
    } else {
      return {
        ap_id: "AP-GENERIC-01",
        location: location || "VFSTR Main Campus",
        status: "HEALTHY" as const,
        packet_loss_pct: 0.0,
        latency_ms: 12,
        jitter_ms: 1.2,
        rssi_dbm: -48,
        bandwidth_mbps: 500.0,
        connected_clients: 45,
        mqtt_topic: "vfstr/telemetry/main/ap_01",
        detail: "SNMP Telemetry Socket healthy"
      };
    }
  }
}
