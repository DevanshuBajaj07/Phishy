
# 🛡️ Python Penetration Testing Framework

A lightweight, modular penetration testing tool written in Python. This tool performs basic reconnaissance, vulnerability scanning, and simulated exploitation of common web vulnerabilities — all with auto-generated reports in both **TXT** and **PDF** formats.

---

## 📦 Features

- 🌐 **Reconnaissance**:  
  - DNS & IP resolution  
  - HTTP header analysis  
  - `robots.txt` scraping  
  - WHOIS lookup

- 🔍 **Scanning**:  
  - Nmap-based port and service scanning  
  - Simulated CVE detection for known services

- 💥 **Exploitation (Simulated)**:  
  - Weak credential brute force  
  - SQL Injection detection  
  - Reflected XSS injection  
  - File upload form detection

- 📝 **Reporting**:  
  - TXT and PDF report generation  
  - Includes findings, severity, and remediation tips

---

## 🛠️ Installation

### ✅ Requirements

- Python 3.7+
- `pip` (Python package manager)
- `nmap` (must be installed and accessible from command line)
- Internet access (for live scanning)
- Dependencies listed below

### 📥 Install Packages

Before using the tool, install the following dependencies:

```bash
pip install requests python-whois reportlab
```

> Make sure `nmap` is installed and added to your system path:
- On Linux/macOS: `sudo apt install nmap` or `brew install nmap`
- On Windows: [Download Nmap](https://nmap.org/download.html)

---

## 🚀 Usage

Run the tool from the terminal:

```bash
python main.py
```

You’ll be presented with a menu:

```
Select Scan Option:
1. Full Scan
2. Reconnaissance Only
3. Vulnerability Scan Only
4. Exploitation Only
5. Exit
```

Enter the URL you want to scan (e.g., `http://testphp.vulnweb.com`) and select an option.

### 📁 Reports

After the scan completes, reports will be saved in your working directory:
- `pentest_report.txt`
- `pentest_report.pdf`

---

## 📂 Project Structure

```
.
├── main.py          # Entry point with CLI menu
├── recon.py         # Reconnaissance module
├── scanner.py       # Port scanning & CVE check
├── exploit.py       # Simulated exploitation module
├── reporter.py      # Report generation (TXT + PDF)
├── README.md        # You're reading it!
```

---

## 💡 Example Target (Practice)

Try scanning this intentionally vulnerable website:
```
http://testphp.vulnweb.com
```

---

## ⚠️ Legal Disclaimer

This tool is for **educational and ethical hacking purposes only**. Do not scan or attack any system without **explicit permission**. Unauthorized access is illegal.

---

## 🧠 Author Notes

Built as a learning project to demonstrate how different phases of penetration testing work — from recon to reporting — all in Python. Pull requests and suggestions are welcome!

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).
