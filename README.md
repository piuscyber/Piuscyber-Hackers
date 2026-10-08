# Piuscyber-Hackers v3.0 PRO - Ethical Network Auditor

> For Educational & Authorized Security Testing Only

This tool is built by Payo (Piuscyber Lab - Ado-Ekiti) to learn how to SECURE CCTV/DVR systems, not to break them.

### 🎯 Purpose
As an aspiring Ethical Hacker, I built this to understand how attackers find open cameras, so I can help home and small businesses close those doors.

### ⚡ Features
- Fast multi-threaded port scanning (50 threads)
- CCTV fingerprinting: Hikvision, Dahua, Generic IP Cam detection
- Banner grabbing for HTTP/RTSP services
- Auto network discovery (supports 192.168.x.x/24)
- Auto-report generation to Desktop (`Piuscyber-Audit-Report-...txt`)
- Ethical use only - designed for own lab audit

### 🔍 CCTV Ports Checked
`80, 81, 82, 554 (RTSP), 8000, 8080, 8443, 37777 (Dahua), 8899, 10554`

### 🚀 How to Use (Your Own Lab Only)
```bash
pip install colorama
python piuscyber-pro.py
# Enter your local network e.g 192.168.40.0/24