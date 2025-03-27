# main.py
# Entry point for the Pentest Framework.
# Allows user to interactively select what type of scan to run on a target URL.

from recon import run_recon
from scanner import run_scan
from exploit import run_exploits
from reporter import Reporter

def full_scan(target_url, reporter):
    """
    Runs a full scan:
    1. Reconnaissance
    2. Vulnerability Scan (open ports + simulated CVE checks)
    3. Exploitation (simulated attacks)
    Saves results into TXT and PDF reports.
    """
    hostname, ip = run_recon(target_url, reporter)

    # If IP address couldn't be resolved, skip scanning
    if ip:
        run_scan(ip, reporter)

    run_exploits(target_url, reporter)
    reporter.finalize()

def menu():
    """
    Presents a simple text menu to the user.
    User can choose the type of scan and enter a URL.
    """
    # Create a new reporter instance
    reporter = Reporter()

    # Ask user to input a URL
    target = input("Enter target URL (e.g., http://testphp.vulnweb.com): ").strip()

    # Loop until valid option is selected
    while True:
        print("\nSelect Scan Option:")
        print("1. Full Scan")
        print("2. Reconnaissance Only")
        print("3. Vulnerability Scan Only")
        print("4. Exploitation Only")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            full_scan(target, reporter)
            break
        elif choice == "2":
            run_recon(target, reporter)
            reporter.finalize()
            break
        elif choice == "3":
            hostname, ip = run_recon(target, reporter)
            if ip:
                run_scan(ip, reporter)
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

# Entry point for the script
if __name__ == "__main__":
    menu()
