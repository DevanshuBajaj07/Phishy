# reporter.py - Handles saving scan results to TXT and HTML reports

from datetime import datetime
import os
from colorama import Fore  # For colored output

# Default text file report name
DEFAULT_TXT_REPORT = "pentest_report.txt"

class Reporter:
    """
    Reporter class is responsible for collecting and exporting results
    into readable TXT and styled HTML reports.
    """
    def __init__(self, txt_filename=DEFAULT_TXT_REPORT):
        self.txt_filename = txt_filename
        self.sections = []  # List of (title, content) sections
        self.clear_reports()  # Reset existing reports when initialized

    def clear_reports(self):
        """
        Clear the TXT report file and reset the section list.
        """
        try:
            open(self.txt_filename, "w").close()
            self.sections.clear()
            print(Fore.CYAN + f"[*] Starting fresh report: {self.txt_filename}")
        except Exception as e:
            print(Fore.RED + f"[!] Error clearing TXT report: {str(e)}")

    def add_section(self, title, content):
        """
        Add a titled section to the report and write to the TXT file immediately.
        """
        self.sections.append((title, content))
        try:
            with open(self.txt_filename, "a", encoding="utf-8") as f:
                f.write(f"\n## {title} ##\n{content}\n")
        except Exception as e:
            print(Fore.RED + f"[!] Error writing to TXT report: {str(e)}")

    def finalize(self):
        """
        Finalize the report generation by saving the HTML report.
        """
        self.save_html_report()
        print(Fore.GREEN + f"\n[+] Reports saved to:\n - {self.txt_filename}\n - pentest_report.html")

    def save_html_report(self):
        """
        Convert report sections into a styled HTML report.
        """
        try:
            with open("pentest_report.html", "w", encoding="utf-8") as f:
                f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Penetration Test Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f8f9fa;
      margin: 30px;
      color: #333;
    }}
    h1 {{
      color: #2c3e50;
      font-size: 28px;
      margin-bottom: 5px;
    }}
    .timestamp {{
      font-size: 14px;
      color: #888;
      margin-bottom: 30px;
    }}
    .section {{
      background-color: #ffffff;
      border-left: 6px solid #dc3545;
      padding: 20px;
      margin-bottom: 20px;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .section h2 {{
      color: #dc3545;
      margin-top: 0;
    }}
    pre {{
      background-color: #f4f4f4;
      padding: 12px;
      border-radius: 4px;
      overflow-x: auto;
      font-size: 14px;
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <h1>Penetration Testing Report</h1>
  <div class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
""")

                for title, content in self.sections:
                    f.write(f"""
  <div class="section">
    <h2>{title}</h2>
    <pre>{content}</pre>
  </div>
""")

                f.write("</body></html>")
            print(Fore.GREEN + "[+] HTML report saved as: pentest_report.html")
        except Exception as e:
            print(Fore.RED + f"[!] Error saving HTML report: {str(e)}")
