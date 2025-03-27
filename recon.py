# =================== recon.py ===================
# This module performs reconnaissance on the target.
# It collects basic information such as IP address, HTTP headers, and WHOIS data.

import socket
import requests
import whois
from urllib.parse import urlparse
from reporter import Reporter

def get_ip_and_dns(url):
    """
    Resolves the IP address from the given URL.
    Returns both hostname and IP (or None if resolution fails).
    """
    hostname = urlparse(url).hostname
    try:
        ip = socket.gethostbyname(hostname)
        return hostname, ip
    except socket.error:
        return hostname, None

def fetch_headers(url):
    """
    Fetches and returns HTTP headers of the given URL.
    """
    try:
        r = requests.get(url, timeout=5)
        return "\n".join([f"{k}: {v}" for k, v in r.headers.items()])
    except:
        return "Failed to fetch headers."

def fetch_robots_txt(url):
    """
    Retrieves the content of the robots.txt file.
    """
    try:
        robots_url = url.rstrip("/") + "/robots.txt"
        r = requests.get(robots_url, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
        return "robots.txt not found."
    except:
        return "Failed to fetch robots.txt."

def whois_lookup(hostname):
    """
    Performs a WHOIS lookup to get domain registration info.
    """
    try:
        domain_info = whois.whois(hostname)
        return str(domain_info)
    except:
        return "WHOIS lookup failed."

def run_recon(url, reporter: Reporter):
    """
    Runs all reconnaissance steps and logs them in the report.
    """
    url = url if url.startswith("http") else "http://" + url
    hostname, ip = get_ip_and_dns(url)
    reporter.add_section("Target Information", f"Target: {url}\nHostname: {hostname}\nIP: {ip or 'Unresolved'}")

    headers = fetch_headers(url)
    reporter.add_section("HTTP Headers", headers)

    robots = fetch_robots_txt(url)
    reporter.add_section("robots.txt Content", robots)

    whois_data = whois_lookup(hostname)
    reporter.add_section("WHOIS Information", whois_data)

    return hostname, ip

