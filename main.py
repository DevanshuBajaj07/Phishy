# main.py - Entry point for the Phishy Penetration Testing Framework

import argparse
from colorama import Fore, Style, init  # For colored CLI output
from recon import run_recon
from scanner import run_scan
from exploit import run_exploits
from reporter import Reporter

# Initialize colorama for cross-platform terminal colors
init(autoreset=True)

def banner():
    """Display the welcome banner."""
    print(Fore.CYAN + Style.BRIGHT + "\n🔍 Welcome to Phishy - Modular Pentest Framework\n")

def full_scan(target_url, reporter, nmap_flags="-sV"):
    """
    Run the complete penetration testing sequence:
    - Reconnaissance
    - Scanning
    - Exploitation
    - Report generation
    """
    print(Fore.YELLOW + "[*] Running full scan...")
    hostname, ip = run_recon(target_url, reporter)
    if ip:
        run_scan(ip, reporter, nmap_flags)
    run_exploits(target_url, reporter)
    reporter.finalize()
    print(Fore.GREEN + "[+] Full scan completed. Reports saved.\n")

def menu(nmap_flags="-sV"):
    """
    Display interactive menu to let the user choose which part of the pentest to run.
    """
    banner()
    reporter = Reporter()
    target = input(Fore.YELLOW + "Enter target URL (e.g., http://testphp.vulnweb.com): ").strip()

    while True:
        print(Fore.BLUE + "\nSelect Scan Option:")
        print("1. Full Scan")
        print("2. Reconnaissance Only")
        print("3. Vulnerability Scan Only")
        print("4. Exploitation Only")
        print("5. Exit")

        choice = input(Fore.CYAN + "Enter choice (1-5): ").strip()

        if choice == "1":
            full_scan(target, reporter, nmap_flags)
            break
        elif choice == "2":
            run_recon(target, reporter)
            reporter.finalize()
            break
        elif choice == "3":
            hostname, ip = run_recon(target, reporter)
            if ip:
                run_scan(ip, reporter, nmap_flags)
            reporter.finalize()
            break
        elif choice == "4":
            run_exploits(target, reporter)
            reporter.finalize()
            break
        elif choice == "5":
            print(Fore.RED + "[!] Exiting.")
            break
        else:
            print(Fore.RED + "[!] Invalid option. Please choose between 1-5.")

if __name__ == "__main__":
    # Parse optional Nmap flags from the command line
    parser = argparse.ArgumentParser(description="Phishy - Python Penetration Testing Framework")
    parser.add_argument("--nmap-flags", default="-sV", help="Custom Nmap flags (default: -sV)")
    args = parser.parse_args()
    
    # Launch the menu
    menu(nmap_flags=args.nmap_flags)
