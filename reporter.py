# reporter.py
# Handles saving of scan results to TXT and HTML reports.

from datetime import datetime
import os

DEFAULT_TXT_REPORT = "pentest_report.txt"

class Reporter:
    def __init__(self, txt_filename=DEFAULT_TXT_REPORT):
        self.txt_filename = txt_filename
        self.sections = []
        self.clear_reports()

    def clear_reports(self):
        try:
            open(self.txt_filename, "w").close()
            self.sections.clear()
        except Exception as e:
            print(f"[!] Error clearing TXT report: {str(e)}")

    def add_section(self, title, content):
        self.sections.append((title, content))
        try:
            with open(self.txt_filename, "a", encoding="utf-8") as f:
                f.write(f"\n## {title} ##\n{content}\n")
        except Exception as e:
            print(f"[!] Error writing to TXT report: {str(e)}")

    def finalize(self):
        self.save_html_report()
        print(f"\n[+] Reports saved to:\n - {self.txt_filename}\n - pentest_report.html")

    def save_html_report(self):
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
            print("[+] HTML report saved as: pentest_report.html")
        except Exception as e:
            print(f"[!] Error saving HTML report: {str(e)}")
