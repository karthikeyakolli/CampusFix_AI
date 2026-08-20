# KB-VFSTR-MASTER-001 — Vignan VFSTR Vadlamudi Master Campus Locations & Detailed IT Support Matrix

## 🏛️ 1. Master VFSTR Vadlamudi Campus Locations & Infrastructure

### 1.1 A-Block (NTR Vignan Bhavan — Administrative Hub)
- **Facilities**: Vice Chancellor's Office, Registrar Office, Student Affairs, Admissions Desk, Examination Cell, Accounts & Fee Counter, Main University Auditorium.
- **Key IT Nodes**: `GW-A-BLOCK-01`, `SSO-AUTH-SERVER`, `FEE-GATEWAY-01`.
- **Common Issues**:
  - Examination fee payment gateway pending status on `vignan.ac.in/portal`.
  - Student SSO account password lock after failed attempts.
  - Semester hall ticket PDF download link authorization error.
  - Main Auditorium wireless microphone audio feedback noise.

### 1.2 H-Block (A.P.J. Abdul Kalam Block — CSE, IT, AI & Data Science)
- **Facilities**: Department of Computer Science & Engineering (CSE), Information Technology (IT), AI & Machine Learning, Data Science, Computer Labs 1 to 12, Smart Classrooms H-101 to H-408.
- **Key IT Nodes**: `AP-HBLOCK-CSE-01`, `AP-HBLOCK-CSE-02`, `HPC-CLUSTER-01`.
- **Common Issues**:
  - Smart Board HDMI audio output silent in Smart Classrooms H-102 and H-204.
  - Research HPC server cluster GPU bandwidth throttling during ML training jobs.
  - High 5GHz Wi-Fi channel congestion in CSE Lab 4 and Lab 7.
  - Faculty digital podium touch screen unresponsive.

### 1.3 N-Block (Pharmacy & Bio-Technology Block)
- **Facilities**: Department of Pharmacy, Bio-Technology, Biomedical Engineering, Pharmaceutical Analysis Labs, Bio-Informatics Lab, Classrooms N-101 to N-304.
- **Key IT Nodes**: `AP-NBLOCK-BIO-01`, `LAB-PHARM-SW-01`.
- **Common Issues**:
  - Bio-Informatics workstation ethernet port link down.
  - Digital podium projector lamp flickering in N-104.
  - Specialized Drug Design software license key activation error.

### 1.4 U-Block (Mechanical & Robotics Block)
- **Facilities**: Department of Mechanical Engineering, Robotics & Automation, Mechatronics, CAD/CAM Labs, Workshop, Thermal Lab, Seminar Hall U-201, Classrooms U-101 to U-305.
- **Key IT Nodes**: `AP-UBLOCK-MECH-01`, `CAD-WORKSTATION-HOST`.
- **Common Issues**:
  - Projector lamp dim / display flickering in U-201 Mechanical Seminar Hall.
  - CAD/CAM workstation AutoCAD network license checkout timeout.
  - Workshop CNC machine serial data interface communication error.

### 1.5 P-Block (Civil Engineering Block)
- **Facilities**: Department of Civil Engineering, Hydraulics Lab, Concrete Testing Lab, Surveying Lab, Classrooms P-101 to P-206.
- **Key IT Nodes**: `AP-PBLOCK-CIVIL-01`.
- **Common Issues**:
  - Hybrid lecture recording camera offline in P-101 Civil CAD Hall.
  - Wi-Fi signal attenuation in Concrete Testing Basement Lab.

### 1.6 L-Block (Central Library & Learning Resource Centre)
- **Facilities**: Central Library, Digital Resource Centre, Contactless Print Kiosk (`PRN-LIB-01`), E-Journals Station, Quiet Study Zone, Book Counter.
- **Key IT Nodes**: `PRN-LIB-01`, `AP-LIB-DIGITAL`, `PROXY-IEEE-01`.
- **Common Issues**:
  - Contactless Print QR Pass release failure at `PRN-LIB-01` print kiosk.
  - Printer spooler queue jammed or paper tray empty error.
  - IEEE Xplore & ScienceDirect e-journal remote proxy access access denied.
  - RFID book self-checkout scanner sensor error code E-902.
  - Air conditioning cooling insufficient in Digital Library section.

### 1.7 Hostel B (Boys Residence Hostel)
- **Facilities**: Rooms 101 to 450, Hostel Mess Hall, Dining Hall, Resident Warden Office, Student Laundry.
- **Key IT Nodes**: `AP-HB-01` to `AP-HB-12` (Access Point AP-HB-04 covers Rooms 201-220).
- **Common Issues**:
  - `VFSTR-STUDENT` Wi-Fi access point `AP-HB-04` high packet loss and disconnection in Rooms 201-220.
  - DHCP IP address pool exhaustion on mobile devices during peak evening hours (8 PM - 11 PM).
  - Power socket voltage fluctuation in Hostel B Room 304.
  - Hostel mess hall Wi-Fi captive portal redirect page timeout.

### 1.8 Priyadarshini Girls Hostel (Girls Residence)
- **Facilities**: Rooms 101 to 400, Study Lounge, Girls Hostel Security Gate, Resident Mess Hall.
- **Key IT Nodes**: `AP-PGH-01` to `AP-PGH-10`.
- **Common Issues**:
  - Wi-Fi signal drop in Priyadarshini Girls Hostel Block A Rooms 105-120.
  - Biometric face recognition gate entry scanner slow response at 10 PM curfew.
  - RO Water Purifier filter maintenance warning indicator in Block B.

---

## 🔧 2. Comprehensive Problem & Troubleshooting Matrix

| Issue ID | Category | Location | Problem Description | Automated Resolution Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **VFSTR-WIFI-01** | Wi-Fi | Hostel B (Rooms 201-220) | `AP-HB-04` packet loss / frequent disconnection | Executed automated AP reset. Dispatched field technician. ETA: 15 mins. |
| **VFSTR-WIFI-02** | Wi-Fi | Priyadarshini Girls Hostel | DHCP IP pool exhaustion on `VFSTR-STUDENT` | Expanded DHCP lease pool & flushed stale leases. |
| **VFSTR-WIFI-03** | Wi-Fi | H-Block CSE Labs | 5GHz channel co-channel interference | Auto-channel optimization executed (`AP-HBLOCK-CSE-01`). |
| **VFSTR-SSO-01** | SSO Auth | `vignan.ac.in/portal` | Account locked after 3 failed password attempts | Triggered automated identity verification & SMS OTP reset link. |
| **VFSTR-SSO-02** | SSO Auth | Exam Cell Portal | Semester Fee Payment status pending after bank debit | Re-queried bank gateway API. Auto-reconciled transaction status. |
| **VFSTR-AV-01** | Smart Classroom | H-Block H-102 | Smart Board HDMI audio output silent | Emergency AV Specialist dispatched. Technician ETA: 3 mins. |
| **VFSTR-AV-02** | Smart Classroom | U-Block U-201 | Projector lamp dim / flickering in Seminar Hall | Replacement projector unit ticket queued for Maintenance. |
| **VFSTR-PRN-01** | Printing | Central Library (L-Block) | Contactless Print QR Pass failed at `PRN-LIB-01` | Reset print spooler queue on server `PRN-LIB-01`. |
| **VFSTR-PRN-02** | Printing | Central Library | IEEE / ScienceDirect e-journal remote proxy error | Refreshed EZProxy token authorization for student Roll Number. |
