# recon.py - Performs reconnaissance: DNS/IP resolution, HTTP headers, robots.txt, WHOIS
import socket
import requests
import whois
from tqdm import tqdm  # For progress bar
from colorama import Fore  # For colored output
from urllib.parse import urlparse
from reporter import Reporter

def get_ip_and_dns(url):
    """
    Resolve the hostname and IP address from the given URL.
    """
    hostname = urlparse(url).hostname
    print(Fore.CYAN + "[*] Resolving hostname and IP...")
    try:
        ip = socket.gethostbyname(hostname)
        print(Fore.GREEN + f"[+] Hostname: {hostname}")
        print(Fore.GREEN + f"[+] IP Address: {ip}")
        return hostname, ip
    except socket.gaierror:
        print(Fore.RED + f"[-] Could not resolve IP for: {hostname}")
        return hostname, None

def fetch_headers(url):
    """
    Retrieve HTTP headers from the target URL.
    """
    print(Fore.CYAN + "[*] Fetching HTTP headers...")
    try:
        response = requests.get(url, timeout=5)
        return "\n".join(f"{k}: {v}" for k, v in response.headers.items())
    except requests.RequestException as e:
        return f"Error fetching headers: {e}"

def fetch_robots_txt(url):
    """
    Try to retrieve robots.txt content.
    """
    print(Fore.CYAN + "[*] Checking for robots.txt...")
    try:
        robots_url = f"{url.rstrip('/')}/robots.txt"
        response = requests.get(robots_url, timeout=5)
        return response.text if response.status_code == 200 else "robots.txt not found."
    except requests.RequestException as e:
        return f"Error fetching robots.txt: {e}"

def whois_lookup(hostname):
    """
    Perform a WHOIS domain lookup.
    """
    print(Fore.CYAN + "[*] Performing WHOIS lookup...")
    try:
        return str(whois.whois(hostname))
    except Exception as e:
        return f"WHOIS lookup failed: {e}"

def run_recon(url, reporter: Reporter):
    """
    Executes all reconnaissance steps and logs results using the Reporter.
    """
    url = url if url.startswith("http") else "http://" + url

    # Display progress using tqdm
    for step in tqdm(["Resolving DNS", "Fetching headers", "Checking robots.txt", "WHOIS lookup"], desc="Recon Module"):
        pass  # purely for animation effect (as real steps are below)

    # Perform actual recon operations
    hostname, ip = get_ip_and_dns(url)
    reporter.add_section("Target Information", f"URL: {url}\nHostname: {hostname}\nIP: {ip or 'Not resolved'}")

    headers = fetch_headers(url)
    reporter.add_section("HTTP Headers", headers)

    robots = fetch_robots_txt(url)
    reporter.add_section("robots.txt", robots)

    whois_data = whois_lookup(hostname)
    reporter.add_section("WHOIS Information", whois_data)

    return hostname, ip
