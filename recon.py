# recon.py - Performs reconnaissance: DNS/IP, headers, robots.txt, WHOIS
import socket, requests, whois
from urllib.parse import urlparse
from reporter import Reporter

def get_ip_and_dns(url):
    # Resolve the hostname and IP from URL
    hostname = urlparse(url).hostname
    try:
        ip = socket.gethostbyname(hostname)
        return hostname, ip
    except socket.gaierror:
        return hostname, None

def fetch_headers(url):
    # Fetch HTTP headers from target
    try:
        response = requests.get(url, timeout=5)
        return "\n".join(f"{k}: {v}" for k, v in response.headers.items())
    except requests.RequestException as e:
        return f"Error fetching headers: {e}"

def fetch_robots_txt(url):
    # Retrieve robots.txt content
    try:
        robots_url = f"{url.rstrip('/')}/robots.txt"
        response = requests.get(robots_url, timeout=5)
        return response.text if response.status_code == 200 else "robots.txt not found."
    except requests.RequestException as e:
        return f"Error fetching robots.txt: {e}"

def whois_lookup(hostname):
    # Perform WHOIS lookup for domain information
    try:
        return str(whois.whois(hostname))
    except Exception as e:
        return f"WHOIS lookup failed: {e}"

def run_recon(url, reporter: Reporter):
    # Execute all reconnaissance steps
    url = url if url.startswith("http") else "http://" + url
    hostname, ip = get_ip_and_dns(url)

    reporter.add_section("Target Information", f"URL: {url}\nHostname: {hostname}\nIP: {ip or 'Not resolved'}")
    reporter.add_section("HTTP Headers", fetch_headers(url))
    reporter.add_section("robots.txt", fetch_robots_txt(url))
    reporter.add_section("WHOIS Information", whois_lookup(hostname))

    return hostname, ip
