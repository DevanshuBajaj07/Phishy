
# main.py
# Entry point for the Pentest Framework.
# Allows user to interactively select what type of scan to run on a target URL.

import argparse
from recon import run_recon
from scanner import run_scan
from exploit import run_exploits
from reporter import Reporter

def full_scan(target_url, reporter, nmap_flags="-sV"):
    """
    Runs a full scan:
    1. Reconnaissance
    2. Vulnerability Scan
    3. Exploitation
    """
    hostname, ip = run_recon(target_url, reporter)
    if ip:
        run_scan(ip, reporter, nmap_flags=nmap_flags)
    run_exploits(target_url, reporter)
    reporter.finalize()

def menu(nmap_flags="-sV"):
    """
    Presents a menu for scan selection.
    """
    reporter = Reporter()
    target = input("Enter target URL (e.g., http://testphp.vulnweb.com): ").strip()

    while True:
        print("\nSelect Scan Option:")
        print("1. Full Scan")
        print("2. Reconnaissance Only")
        print("3. Vulnerability Scan Only")
        print("4. Exploitation Only")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            full_scan(target, reporter, nmap_flags=nmap_flags)
            break
        elif choice == "2":
            run_recon(target, reporter)
            reporter.finalize()
            break
        elif choice == "3":
            hostname, ip = run_recon(target, reporter)
            if ip:
                run_scan(ip, reporter, nmap_flags=nmap_flags)
            reporter.finalize()
            break
        elif choice == "4":
            run_exploits(target, reporter)
            reporter.finalize()
            break
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Pentest Framework")
    parser.add_argument("--nmap-flags", default="-sV", help="Custom Nmap scan flags (default: -sV)")
    args = parser.parse_args()

    menu(nmap_flags=args.nmap_flags)
