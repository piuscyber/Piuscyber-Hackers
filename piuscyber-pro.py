#!/usr/bin/env python3
"""
Piuscyber-Hackers v3.0 PRO - Ethical Auditor + Report Generator
For EDUCATIONAL & AUTHORIZED TESTING ONLY
Author: Payo (Piuscyber Lab)
"""

import socket
import sys
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import ipaddress
from colorama import Fore, Style, init

init(autoreset=True)

CCTV_PORTS = {
    80: "HTTP (Web Panel)", 81: "HTTP Alt", 82: "HTTP Alt",
    554: "RTSP Stream", 8000: "DVR/NVR SDK", 8080: "HTTP Alt / Cam Web",
    8443: "HTTPS Alt", 37777: "Dahua TCP", 37778: "Dahua UDP Alt",
    8899: "Hikvision/Some DVR", 10554: "RTSP Alt"
}

REPORT_LOG = []

def banner():
    print(Fore.CYAN + r"""
  ____  _             ____       _               ____  ____   ___  
 |  _ \(_) __ _  ___ / ___|_   _| |__   ___ _ __|  _ \|  _ \ / _ \ 
 | |_) | |/ _` |/ __| |   | | | | '_ \ / _ \ '__| | | | |_) | | | |
 |  __/| | (_| |\__ \ |___| |_| | |_) |  __/ |  | |_| |  _ <| |_| |
 |_|   |_|\__,_||___/\____|\__, |_.__/ \___|_|  |____/|_| \_\\___/ 
                           |___/                                   
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "  Piuscyber-Hackers v3.0 PRO | Report Edition" + Style.RESET_ALL)
    print(Fore.GREEN + "  [*] Ethical Use Only - Secure Your Own Lab" + Style.RESET_ALL)
    print("-"*70)

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1.5)
        s.connect((ip, port))
        if port in [80, 8080, 81, 82, 8000, 8443]:
            s.send(b"GET / HTTP/1.0\r\n\r\n")
        b = s.recv(1024).decode(errors="ignore")
        s.close()
        if "Hikvision" in b: return "Likely Hikvision"
        if "Dahua" in b or "DH-" in b: return "Likely Dahua"
        if "Hipcam" in b: return "Generic IP Cam"
        if "Server:" in b: return b.split("Server:")[1].split("\r\n")[0].strip()[:30]
        return "No banner / filtered"
    except:
        return "No banner"

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        if result == 0:
            info = CCTV_PORTS.get(port, "Unknown")
            banner_info = grab_banner(str(ip), port)
            line = f"[+] OPEN Port {port} ({info}) on {ip} | Fingerprint: {banner_info}"
            print(Fore.GREEN + line + Style.RESET_ALL)
            REPORT_LOG.append(line)
            return True
        return False
    except:
        return False

def scan_target(target):
    header = f"\n[*] Scanning {target} at {datetime.now()}"
    print(Fore.YELLOW + header + Style.RESET_ALL)
    REPORT_LOG.append(header)
    found = 0
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda p: scan_port(target, p), CCTV_PORTS.keys()))
        found = sum(results)
    
    if found == 0:
        msg = f"[-] {target} -> No CCTV ports open (Secure / Not a camera)"
        print(Fore.RED + msg + Style.RESET_ALL)
        REPORT_LOG.append(msg)
    else:
        msg = f"[REPORT] {target} has {found} open camera services."
        print(Fore.CYAN + msg + Style.RESET_ALL)
        REPORT_LOG.append(msg)
    REPORT_LOG.append("-"*50)

def save_report():
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
            desktop = os.getcwd()
        filename = f"Piuscyber-Audit-Report-{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
        path = os.path.join(desktop, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write("Piuscyber-Hackers v3.0 - Ethical Audit Report\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Operator: Payo - Piuscyber Lab\n")
            f.write("Disclaimer: For authorized educational testing only.\n")
            f.write("="*60 + "\n\n")
            for line in REPORT_LOG:
                f.write(line + "\n")
            f.write("\n[RECOMMENDATIONS]\n")
            f.write("1. Change default passwords\n2. Update firmware\n3. Disable unused ports\n4. Isolate CCTV on separate VLAN\n")
        print(Fore.GREEN + f"\n[✓] Report saved to: {path}" + Style.RESET_ALL)
    except Exception as e:
        print(f"[!] Could not save report: {e}")

def main():
    banner()
    print(Fore.WHITE + "WARNING: Only scan networks you OWN or have WRITTEN permission.\n")
    target = input(Fore.CYAN + "Enter target (IP or 192.168.48.0/24): " + Style.RESET_ALL).strip()
    if not target:
        sys.exit()

    try:
        if "/" in target:
            net = ipaddress.ip_network(target, strict=False)
            print(Fore.YELLOW + f"[*] PRO MODE: Scanning {net} - {net.num_addresses} hosts" + Style.RESET_ALL)
            REPORT_LOG.append(f"Network scan: {net}")
            # Limit to 254 for home lab to be fast
            for ip in net.hosts():
                scan_target(ip)
        else:
            scan_target(target)

        save_report()
        print(Fore.YELLOW + "\n[+] Audit Complete. You are now thinking like a defender!" + Style.RESET_ALL)

    except KeyboardInterrupt:
        print("\n[!] Stopped.")
        save_report()

if __name__ == "__main__":
    main()