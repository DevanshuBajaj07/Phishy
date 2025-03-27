# scanner.py
# This module performs network scanning using Nmap and simulates basic vulnerability detection.

import subprocess
from reporter import Reporter

def nmap_service_scan(ip):
    """
    Uses Nmap to scan the target IP address for open ports and running services.
    Returns a formatted string for the report and a list of found services.
    """
    try:
        # Run the Nmap command with -sV to detect service versions
        result = subprocess.check_output(["nmap", "-sV", ip], stderr=subprocess.STDOUT).decode()

        table = []  # Store tuples of (port, state, service name)
        for line in result.splitlines():
            # We're interested in lines with 'tcp' or 'udp' and an 'open' state
            if any(proto in line for proto in ["tcp", "udp"]) and "open" in line:
                parts = line.split()
                if len(parts) >= 3:
                    # Example line: "80/tcp open http"
                    table.append((parts[0], parts[1], " ".join(parts[2:])))  # e.g. ('80/tcp', 'open', 'http')

        if not table:
            return "No open ports detected.", []

        # Format the output nicely for the report
        formatted = "\n".join([f"{p:<10} {s:<10} {n}" for p, s, n in table])
        return formatted, table

    except subprocess.CalledProcessError as e:
        # If Nmap returns a non-zero exit code (usually due to errors), show output
        return f"Nmap scan failed:\n{e.output.decode()}", []

    except FileNotFoundError:
        # Nmap is not installed or not found in PATH
        return "Nmap is not installed or not found in your system PATH.", []

    except Exception as e:
        # Any other unexpected error
        return f"Unexpected error during Nmap scan: {str(e)}", []

def simulated_cve_check(services):
    """
    Simulates a CVE check by comparing known vulnerable services.
    Each matched service is given a severity level and suggested remediation.
    """
    # Simulated database of vulnerable services (just a few examples)
    known_issues = {
        "Apache": ("Medium", "Ensure the latest version is patched."),
        "OpenSSH": ("High", "Restrict SSH access and keep OpenSSH updated."),
        "MySQL": ("High", "Update MySQL and restrict database access."),
    }

    findings = []

    # Check each service name against known issues
    for _, _, service in services:
        for keyword in known_issues:
            if keyword.lower() in service.lower():
                severity, fix = known_issues[keyword]
                findings.append((keyword, severity, fix))

    # Format results for reporting
    if not findings:
        return "No known vulnerable services found."

    return "\n".join([f"{service} - Severity: {severity}\nRemediation: {fix}" for service, severity, fix in findings])

def run_scan(ip, reporter: Reporter):
    """
    Runs the full scan process:
    1. Nmap port and service discovery
    2. Simulated CVE check
    Results are added to the final report.
    """
    nmap_result, services = nmap_service_scan(ip)
    reporter.add_section("Open Ports and Services", nmap_result)

    if services:
        cve_result = simulated_cve_check(services)
        reporter.add_section("Known Vulnerability Check (Simulated)", cve_result)
