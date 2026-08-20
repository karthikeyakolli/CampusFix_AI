# KB-VFSTR-STUDENT-001 — Vignan VFSTR Student IT Support & Troubleshooting Protocols

## 1. Student Wi-Fi Access (`VFSTR-STUDENT`)
- **Symptoms**: Disconnection in Hostel B or Priyadarshini Girls Hostel, "Authentication Failed" error when connecting to `VFSTR-STUDENT`.
- **Diagnostic Procedure**:
  1. Verify student status is active in directory database.
  2. Ping local Access Point (e.g. `AP-HB-04` in Hostel B or `AP-PGH-02` in Priyadarshini Hostel).
  3. If packet loss exceeds 50%, escalate candidate incident to Vignan Network Operations Team.
  4. Instruct student to forget network `VFSTR-STUDENT` and re-enter Vignan Roll Number credentials.

## 2. Vignan Student Portal & SSO Login Failure (`https://vignan.ac.in/portal`)
- **Symptoms**: Invalid password message, locked account after 3 failed login attempts, missing attendance/marks tab.
- **Protocol**:
  - Never request student password.
  - Verify account is unlocked in directory.
  - Guide student to official Vignan Self-Service Password Reset Portal (`https://vignan.ac.in/reset`).

## 3. Central Library Digital Printing (`PRN-LIB-01`)
- **Symptoms**: Print job stuck in queue at Central Library (L-Block), paper jam sensor error.
- **Protocol**:
  - Run `check_printer_queue('PRN-LIB-01')`.
  - If hardware jam is detected, dispatch Ticket to Library IT Helpdesk assistant for physical paper tray clearance.
