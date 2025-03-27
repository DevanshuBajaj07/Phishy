# =================== main.py ===================
# This file provides the entry point and user interface for the penetration testing tool.

from recon import run_recon
from scanner import run_scan
from exploit import run_exploits
from reporter import Reporter

def full_scan(target_url, reporter):
    """
    Performs a full scan: recon -> scan -> exploit.
    """
    hostname, ip = run_recon(target_url, reporter)
    if ip:
        run_scan(ip, reporter)
    run_exploits(target_url, reporter)
    reporter.finalize()

def menu():
    """
    Provides a CLI menu to choose between different scan options.
    """
    reporter = Reporter()
    target = input("Enter target URL (e.g., http://testphp.vulnweb.com): ").strip()
    print("\nSelect Scan Option:")
    print("1. Full Scan")
    print("2. Reconnaissance Only")
    print("3. Vulnerability Scan Only")
    print("4. Exploitation Only")
    print("5. Exit")

    choice = input("Enter choice: ")
    if choice == "1":
        full_scan(target, reporter)
    elif choice == "2":
        run_recon(target, reporter)
        reporter.finalize()
    elif choice == "3":
        hostname, ip = run_recon(target, reporter)
        if ip:
            run_scan(ip, reporter)
        reporter.finalize()
    elif choice == "4":
        run_exploits(target, reporter)
        reporter.finalize()
    else:
        print("Exiting.")

if __name__ == "__main__":
    menu()
