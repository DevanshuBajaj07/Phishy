# recon.py
# This module performs reconnaissance on a given URL, including DNS/IP lookup, header collection,
# robots.txt retrieval, and WHOIS lookup.

import socket
import requests
import whois
from urllib.parse import urlparse
from reporter import Reporter

def get_ip_and_dns(url):
    """
    Resolves the IP address from the given URL using socket.
    Returns both hostname and IP address (or None if resolution fails).
    """
    hostname = urlparse(url).hostname
    try:
        ip = socket.gethostbyname(hostname)
        return hostname, ip
    except socket.gaierror as e:
        # DNS resolution failure (e.g., host not found)
        return hostname, None

def fetch_headers(url):
    """
    Sends an HTTP GET request to fetch and return all response headers.
    Returns headers in a readable key: value format.
    """
    try:
        response = requests.get(url, timeout=5)
        return "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
    except requests.exceptions.RequestException as e:
        # Network timeout, connection error, or invalid response
        return f"Failed to fetch headers: {str(e)}"

def fetch_robots_txt(url):
    """
    Tries to retrieve the contents of the robots.txt file from the target.
    This file often contains disallowed paths useful for further exploration.
    """
    try:
        robots_url = url.rstrip("/") + "/robots.txt"
        response = requests.get(robots_url, timeout=5)

        if response.status_code == 200:
            return response.text.strip()
        return f"robots.txt not found (Status Code: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch robots.txt: {str(e)}"

def whois_lookup(hostname):
    """
    Performs a WHOIS lookup to gather domain ownership and registration data.
    This often includes registrar, admin contacts, and expiry dates.
    """
    try:
        domain_info = whois.whois(hostname)
        return str(domain_info)
    except Exception as e:
        # The whois library throws generic exceptions (e.g., if domain has no WHOIS entry)
        return f"WHOIS lookup failed: {str(e)}"

def run_recon(url, reporter: Reporter):
    """
    Master function to run all recon steps:
    1. DNS/IP resolution
    2. HTTP headers fetch
    3. robots.txt check
    4. WHOIS information lookup
    Each section is added to the final report.
    """
    # Ensure the URL starts with http:// or https://
    url = url if url.startswith("http") else "http://" + url

    # Get hostname and IP address
    hostname, ip = get_ip_and_dns(url)
    reporter.add_section("Target Information", f"Target: {url}\nHostname: {hostname}\nIP: {ip or 'Unresolved'}")

    # Fetch and log HTTP headers
    headers = fetch_headers(url)
    reporter.add_section("HTTP Headers", headers)

    # Check for robots.txt
    robots = fetch_robots_txt(url)
    reporter.add_section("robots.txt Content", robots)

    # WHOIS domain lookup
    whois_data = whois_lookup(hostname)
    reporter.add_section("WHOIS Information", whois_data)

    return hostname, ip
