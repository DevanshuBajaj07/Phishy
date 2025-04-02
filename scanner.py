# scanner.py - Performs network scans and vulnerability checks
import subprocess
from reporter import Reporter

def nmap_service_scan(ip, flags="-sV"):
    # Nmap scan for open ports and service detection
    try:
        args = ["nmap"] + flags.split() + [ip]
        output = subprocess.check_output(args, stderr=subprocess.STDOUT).decode()

        services = [(p.split()[0], p.split()[1], " ".join(p.split()[2:]))
                    for p in output.splitlines() if ("tcp" in p or "udp" in p) and "open" in p]

        formatted = "\n".join([f"{p:<10} {s:<10} {n}" for p, s, n in services]) or "No open ports."
        return formatted, services
    except subprocess.CalledProcessError as e:
        return f"Nmap scan error: {e.output.decode()}", []
    except FileNotFoundError:
        return "Nmap not found. Ensure it's installed.", []
    except Exception as e:
        return f"Unexpected error: {e}", []

def simulated_cve_check(services):
    # Basic CVE check simulation
    known_issues = {
        "Apache": ("Medium", "Update Apache."),
        "OpenSSH": ("High", "Restrict SSH and update."),
        "MySQL": ("High", "Secure and update MySQL."),
    }
    findings = [(k, *known_issues[k]) for _, _, s in services for k in known_issues if k.lower() in s.lower()]
    return "\n".join(f"{s} - Severity: {sev}\nRemediation: {r}" for s, sev, r in findings) or "No issues."

def run_scan(ip, reporter: Reporter, nmap_flags="-sV"):
    # Run Nmap scan and CVE checks
    nmap_result, services = nmap_service_scan(ip, nmap_flags)
    reporter.add_section("Open Ports & Services", nmap_result)
    reporter.add_section("Vulnerability Check", simulated_cve_check(services))
