
# 🛡️ Python Penetration Testing Framework

A modular and extensible penetration testing framework built in Python. It performs reconnaissance, vulnerability scanning, simulated exploits, and generates detailed multi-format reports (TXT, PDF, JSON, HTML).

---

## 📦 Features

- 🌐 **Reconnaissance**
  - DNS & IP resolution
  - HTTP header inspection
  - `robots.txt` discovery
  - WHOIS domain lookup

- 🔍 **Scanning**
  - Port and service discovery using Nmap
  - Simulated vulnerability detection for known services (CVE-like)

- 💥 **Exploitation (Simulated)**
  - Weak login credential testing (brute force with common combos)
  - SQL Injection simulation
  - XSS Injection detection
  - File upload form detection

- 📝 **Reporting**
  - Multiple report formats:
    - ✅ Text (.txt)
    - ✅ PDF (.pdf)
    - ✅ JSON (.json)
    - ✅ HTML (.html)
  - Severity-based filtering for JSON/HTML
  - Auto-timestamped metadata

---

## 🛠️ Installation

### ✅ Requirements

- Python 3.7+
- pip
- `nmap` installed on your system and accessible via command line
- Internet access for scans

### 📥 Install Python Dependencies

```bash
pip install requests python-whois reportlab
```

> Make sure `nmap` is installed and in your system PATH:
- Linux: `sudo apt install nmap`
- macOS: `brew install nmap`
- Windows: [Download Nmap](https://nmap.org/download.html)

---

## 🚀 Usage

Run the tool via terminal:

```bash
python main.py
```

You will see an interactive menu like this:

```
Enter target URL (e.g., http://testphp.vulnweb.com):

Select Scan Option:
1. Full Scan
2. Reconnaissance Only
3. Vulnerability Scan Only
4. Exploitation Only
5. Exit
```

Choose your desired scan mode, and the tool will start scanning the given target.

---

## 📂 Report Outputs

After scanning, the following files will be created in the working directory:

| File                | Format  | Purpose                     |
|---------------------|---------|-----------------------------|
| `pentest_report.txt`  | TXT     | Raw, plain-text report      |
| `pentest_report.pdf`  | PDF     | Printable report            |
| `pentest_report.json` | JSON    | Structured, machine-readable|
| `pentest_report.html` | HTML    | Stylish browser-viewable    |

You can configure severity filters (e.g., only include Medium+ findings) in the code.

---

## 📁 Project Structure

```
.
├── main.py           # Entry point CLI menu
├── recon.py          # Reconnaissance logic
├── scanner.py        # Port/CVE scan logic
├── exploit.py        # Simulated attack checks
├── reporter.py       # Multi-format reporting system
├── README.md         # You're reading it!
```

---

## ⚠️ Disclaimer

This tool is for **educational and authorized testing purposes only**.  
Do not scan or attack systems without **explicit permission**. Unauthorized usage is illegal and unethical.

---

## 🧠 Author Notes

This project was built to demonstrate how basic penetration testing tools can be created in Python.  
PRs, suggestions, and ethical hackers welcome!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
