# recon.py
import socket
import requests
import whois
from urllib.parse import urlparse
from reporter import Reporter

def get_ip_and_dns(url):
    hostname = urlparse(url).hostname
    try:
        ip = socket.gethostbyname(hostname)
        return hostname, ip
    except socket.error:
        return hostname, None

def fetch_headers(url):
    try:
        r = requests.get(url, timeout=5)
        return "\n".join([f"{k}: {v}" for k, v in r.headers.items()])
    except:
        return "Failed to fetch headers."

def fetch_robots_txt(url):
    try:
        robots_url = url.rstrip("/") + "/robots.txt"
        r = requests.get(robots_url, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
        return "robots.txt not found."
    except:
        return "Failed to fetch robots.txt."

def whois_lookup(hostname):
    try:
        domain_info = whois.whois(hostname)
        return str(domain_info)
    except:
        return "WHOIS lookup failed."

def run_recon(url, reporter: Reporter):
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
