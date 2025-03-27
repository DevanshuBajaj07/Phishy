
# scanner.py
# This module performs network scanning using Nmap and simulates basic vulnerability detection.

import subprocess
from reporter import Reporter

def nmap_service_scan(ip, flags="-sV"):
    """
    Runs a customizable Nmap scan on the target IP.
    :param ip: Target IP address
    :param flags: Custom Nmap scan flags (default: -sV for version detection)
    :return: Formatted string and parsed list of services
    """
    try:
        # Convert string flags to list (e.g., "-sS -p-" -> ["-sS", "-p-"])
        args = ["nmap"] + flags.split() + [ip]
        result = subprocess.check_output(args, stderr=subprocess.STDOUT).decode()

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
        return f"Nmap scan failed:\n{e.output.decode()}", []
    except FileNotFoundError:
        return "Nmap is not installed or not found in your system PATH.", []
    except Exception as e:
        return f"Unexpected error during Nmap scan: {str(e)}", []

def simulated_cve_check(services):
    """
    Simulates a CVE check by comparing known vulnerable services.
    """
    known_issues = {
        "Apache": ("Medium", "Ensure the latest version is patched."),
        "OpenSSH": ("High", "Restrict SSH access and keep OpenSSH updated."),
        "MySQL": ("High", "Update MySQL and restrict database access."),
    }

    findings = []

    for _, _, service in services:
        for keyword in known_issues:
            if keyword.lower() in service.lower():
                severity, fix = known_issues[keyword]
                findings.append((keyword, severity, fix))

    if not findings:
        return "No known vulnerable services found."

    return "\n".join([f"{service} - Severity: {severity}\nRemediation: {fix}" for service, severity, fix in findings])

def run_scan(ip, reporter: Reporter, nmap_flags="-sV"):
    """
    Runs the scan using Nmap and checks for known vulnerabilities.
    """
    nmap_result, services = nmap_service_scan(ip, flags=nmap_flags)
    reporter.add_section("Open Ports and Services", nmap_result)

    if services:
        cve_result = simulated_cve_check(services)
        reporter.add_section("Known Vulnerability Check (Simulated)", cve_result)
