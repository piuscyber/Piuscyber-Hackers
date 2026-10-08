#!/usr/bin/env python3
# Piuscyber-Hackers - Ethical Scanner
import socket
import os
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT)
    print(r" ____  _               ____       _               ")
    print(r"|  _ \(_)__ _   _ ___ / ___|_   _| |__   ___ _ __ ")
    print(r"| |_) | |/ _` | | / __| |   | | | | '_ \ / _ \ '__|")
    print(r"|  __/| | (_| |_| \__ \ |___| |_| | |_) |  __/ |   ")
    print(r"|_|   |_|\__,_\__,_|___/\___|\__, |_.__/ \___|_|   ")
    print(r"                              |___/                 ")
    print(Fore.YELLOW + "   Piuscyber-Hackers v1.0 | Ethical Use Only\n")

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except:
        return False

def main():
    banner()
    print(Fore.GREEN + "[*] This tool is for YOUR OWN lab only!")
    print(Fore.WHITE + "It will find cameras and help you secure them.\n")
    target = input(Fore.CYAN + "Enter your network target (e.g 192.168.1.1): " + Style.RESET_ALL).strip()
    if "/" in target:
        target = target.split('/')[0]
    ports = {80: "HTTP (Web Cam)", 554: "RTSP (CCTV Stream)", 8080: "HTTP Alt (IP Cam)", 37777: "Dahua CCTV"}
    print(Fore.YELLOW + f"\n[*] Scanning {target} at {datetime.now()}\n")
    found = []
    for port, desc in ports.items():
        if scan_port(target, port):
            print(Fore.GREEN + f"[+] OPEN -> Port {port} : {desc} found on {target}")
            found.append(port)
        else:
            print(Fore.RED + f"[-] CLOSED -> Port {port}")
    if found:
        print(Fore.CYAN + "\n[*] Possible CCTV device detected!")
    else:
        print(Fore.YELLOW + "\n[!] No CCTV ports open on this IP.")

if __name__ == "__main__":
    main()