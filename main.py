# main.py - Entry point for the Pentest Framework
import argparse
from recon import run_recon
from scanner import run_scan
from exploit import run_exploits
from reporter import Reporter

def full_scan(target_url, reporter, nmap_flags="-sV"):
    # Conducts a comprehensive penetration test sequence
    hostname, ip = run_recon(target_url, reporter)
    if ip:
        run_scan(ip, reporter, nmap_flags)
    run_exploits(target_url, reporter)
    reporter.finalize()

def menu(nmap_flags="-sV"):
    # Interactive menu for selecting specific penetration test components
    reporter = Reporter()
    target = input("Enter target URL (e.g., http://testphp.vulnweb.com): ").strip()

    while True:
        print("\nSelect Scan Option:")
        print("1. Full Scan\n2. Reconnaissance Only\n3. Vulnerability Scan Only\n4. Exploitation Only\n5. Exit")
        choice = input("Enter choice (1-5): ").strip()

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
            print("Exiting.")
            break
        else:
            print("Invalid option. Please choose between 1-5.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Penetration Testing Framework")
    parser.add_argument("--nmap-flags", default="-sV", help="Custom Nmap flags (default: -sV)")
    args = parser.parse_args()
    menu(nmap_flags=args.nmap_flags)
