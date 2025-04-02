# scanner.py - Performs network scanning and simulated vulnerability checks

import subprocess
from tqdm import tqdm  # For progress bar
from colorama import Fore  # For colored output
from reporter import Reporter

def nmap_service_scan(ip, flags="-sV"):
    """
    Perform an Nmap scan to detect open ports and services.
    Returns formatted output and structured service list.
    """
    print(Fore.CYAN + f"[*] Starting Nmap scan on {ip} with flags: {flags}")
    try:
        args = ["nmap"] + flags.split() + [ip]
        output = subprocess.check_output(args, stderr=subprocess.STDOUT).decode()

        # Extract lines that represent open TCP/UDP ports
        services = [(p.split()[0], p.split()[1], " ".join(p.split()[2:]))
                    for p in output.splitlines()
                    if ("tcp" in p or "udp" in p) and "open" in p]

        formatted = "\n".join([f"{p:<10} {s:<10} {n}" for p, s, n in services]) or "No open ports."
        print(Fore.GREEN + "[+] Nmap scan completed.")
        return formatted, services
    except subprocess.CalledProcessError as e:
        return f"Nmap scan error: {e.output.decode()}", []
    except FileNotFoundError:
        return "Nmap not found. Please install Nmap on your system.", []
    except Exception as e:
        return f"Unexpected error during scan: {e}", []

def simulated_cve_check(services):
    """
    Simulate vulnerability detection based on known services.
    """
    print(Fore.CYAN + "[*] Running simulated CVE checks...")
    
    # Example known vulnerabilities
    known_issues = {
        "Apache": ("Medium", "Update Apache to the latest version."),
        "OpenSSH": ("High", "Restrict SSH access and update OpenSSH."),
        "MySQL": ("High", "Secure and update MySQL database."),
    }

    # Match services to simulated CVEs
    findings = [(k, *known_issues[k]) for _, _, s in services for k in known_issues if k.lower() in s.lower()]
    if findings:
        print(Fore.RED + f"[!] Found {len(findings)} potential vulnerabilities.")
    else:
        print(Fore.GREEN + "[+] No known vulnerabilities detected.")
    
    return "\n".join(f"{s} - Severity: {sev}\nRemediation: {r}" for s, sev, r in findings) or "No issues detected."

def run_scan(ip, reporter: Reporter, nmap_flags="-sV"):
    """
    Run both Nmap scanning and simulated vulnerability checks.
    """
    # Show progress bar
    for _ in tqdm(range(3), desc="Scanner Module"):
        pass  # purely visual progress indicator

    nmap_result, services = nmap_service_scan(ip, nmap_flags)
    reporter.add_section("Open Ports & Services", nmap_result)

    cve_result = simulated_cve_check(services)
    reporter.add_section("Vulnerability Check", cve_result)
