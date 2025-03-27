# =================== scanner.py ===================
# This module scans the target for open ports and known vulnerabilities.

import subprocess
from reporter import Reporter

def nmap_service_scan(ip):
    """
    Runs a basic Nmap scan to discover open ports and services.
    Returns both raw formatted results and a list of parsed services.
    """
    try:
        result = subprocess.check_output(["nmap", "-sV", ip], stderr=subprocess.STDOUT).decode()
        table = []
        for line in result.splitlines():
            if any(proto in line for proto in ["tcp", "udp"]) and "open" in line:
                parts = line.split()
                if len(parts) >= 3:
                    table.append((parts[0], parts[1], " ".join(parts[2:])))
        if not table:
            return "No open ports detected.", []
        formatted = "\n".join([f"{p:<10} {s:<10} {n}" for p, s, n in table])
        return formatted, table
    except subprocess.CalledProcessError as e:
        return f"Nmap scan failed: {e.output.decode()}", []

def simulated_cve_check(services):
    """
    Simulates a basic CVE check using service names against known issues.
    Returns a summary of simulated vulnerabilities.
    """
    known_issues = {
        "Apache": ("Medium", "Ensure latest version is patched."),
        "OpenSSH": ("High", "Restrict SSH access and keep updated."),
        "MySQL": ("High", "Update MySQL and restrict DB access."),
    }
    findings = []
    for _, _, service in services:
        for keyword in known_issues:
            if keyword.lower() in service.lower():
                severity, fix = known_issues[keyword]
                findings.append((keyword, severity, fix))
    if not findings:
        return "No known vulnerable services found."
    return "\n".join([f"{s} - Severity: {sev}\nRemediation: {fix}" for s, sev, fix in findings])

def run_scan(ip, reporter: Reporter):
    """
    Runs the port and service scan and adds any CVE results to the report.
    """
    nmap_result, services = nmap_service_scan(ip)
    reporter.add_section("Open Ports and Services", nmap_result)
    if services:
        cve_result = simulated_cve_check(services)
        reporter.add_section("Known Vulnerability Check (Simulated)", cve_result)
