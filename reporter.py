
# reporter.py
# Handles saving of scan results to TXT, PDF, JSON, and HTML reports.

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
import json

# Default report filenames
DEFAULT_TXT_REPORT = "pentest_report.txt"
DEFAULT_PDF_REPORT = "pentest_report.pdf"

class Reporter:
    def __init__(self, txt_filename=DEFAULT_TXT_REPORT, pdf_filename=DEFAULT_PDF_REPORT):
        """
        Initializes the reporter.
        - Accepts optional custom filenames for TXT and PDF reports.
        - Clears previous reports if they exist.
        """
        self.txt_filename = txt_filename
        self.pdf_filename = pdf_filename
        self.sections = []  # List of (section title, section content)
        self.clear_reports()

    def clear_reports(self):
        """
        Clears any previous report content.
        - Deletes old PDF file if present.
        - Empties the TXT file.
        """
        try:
            open(self.txt_filename, "w").close()  # Clear TXT file
            if os.path.exists(self.pdf_filename):
                os.remove(self.pdf_filename)  # Delete old PDF
            self.sections.clear()  # Clear in-memory sections
        except Exception as e:
            print(f"[!] Error clearing old reports: {str(e)}")

    def add_section(self, title, content):
        """
        Adds a new section to the report.
        - Saves to in-memory section list
        - Appends to the TXT file immediately
        """
        self.sections.append((title, content))
        try:
            with open(self.txt_filename, "a", encoding="utf-8") as f:
                f.write(f"\n## {title} ##\n{content}\n")
        except Exception as e:
            print(f"[!] Error writing to TXT report: {str(e)}")

    def finalize(self):
        """
        Finalizes the report:
        - Saves TXT (already done in add_section)
        - Generates PDF, JSON, and HTML reports
        """
        self.generate_pdf_report()
        self.save_json_report(min_severity="Low")
        self.save_html_report(min_severity="Low")
        print(f"\n[+] Reports saved to:\n - {self.txt_filename}\n - {self.pdf_filename}\n - pentest_report.json\n - pentest_report.html")

    def generate_pdf_report(self):
        """
        Creates a well-formatted PDF report using ReportLab.
        - Wraps long lines automatically
        - Breaks into pages if needed
        """
        try:
            c = canvas.Canvas(self.pdf_filename, pagesize=letter)
            width, height = letter
            margin = 40
            y = height - margin
            line_height = 14
            max_width = width - 2 * margin

            # Title and timestamp
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y, "Penetration Testing Report")
            y -= line_height
            c.setFont("Helvetica", 12)
            c.drawString(margin, y, "Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            y -= 2 * line_height

            for title, content in self.sections:
                if y < margin + 2 * line_height:
                    c.showPage()
                    y = height - margin
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, y, title)
                underline_width = stringWidth(title, "Helvetica-Bold", 12)
                c.line(margin, y - 1, margin + underline_width, y - 1)
                y -= line_height

                c.setFont("Helvetica", 12)
                for line in content.strip().split("\n"):
                    wrapped_lines = simpleSplit(line.strip(), "Helvetica", 12, max_width)
                    for subline in wrapped_lines:
                        if y < margin + line_height:
                            c.showPage()
                            c.setFont("Helvetica", 12)
                            y = height - margin
                        c.drawString(margin, y, subline)
                        y -= line_height
                y -= line_height

            c.save()
        except Exception as e:
            print(f"[!] Error creating PDF report: {str(e)}")

    def save_json_report(self, min_severity="Low"):
        """
        Saves the findings as a JSON report.
        You can specify a minimum severity to include (Low, Medium, High).
        """
        severity_levels = {"Low": 1, "Medium": 2, "High": 3}
        min_level = severity_levels.get(min_severity, 1)

        report_data = {
            "generated_on": datetime.now().isoformat(),
            "sections": []
        }

        for title, content in self.sections:
            severity = "Low"
            for line in content.splitlines():
                if line.lower().startswith("severity:"):
                    severity = line.split(":")[1].strip().capitalize()
                    break

            if severity_levels.get(severity, 1) >= min_level:
                report_data["sections"].append({
                    "title": title,
                    "severity": severity,
                    "content": content
                })

        try:
            with open("pentest_report.json", "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4)
            print("[+] JSON report saved as: pentest_report.json")
        except Exception as e:
            print(f"[!] Error saving JSON report: {str(e)}")

    def save_html_report(self, min_severity="Low"):
        """
        Generates an HTML report that is easy to view in a browser.
        You can specify a severity threshold to filter sections.
        """
        severity_levels = {"Low": 1, "Medium": 2, "High": 3}
        min_level = severity_levels.get(min_severity, 1)

        try:
            with open("pentest_report.html", "w", encoding="utf-8") as f:
                f.write("<html><head><title>Penetration Test Report</title>")
                f.write("<style>body{font-family:sans-serif;margin:20px;} h2{color:#d32f2f;} pre{background:#f4f4f4;padding:10px;border-left:4px solid #ccc;}</style>")
                f.write("</head><body>")
                f.write(f"<h1>Penetration Testing Report</h1>")
                f.write(f"<p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")

                for title, content in self.sections:
                    severity = "Low"
                    for line in content.splitlines():
                        if line.lower().startswith("severity:"):
                            severity = line.split(":")[1].strip().capitalize()
                            break

                    if severity_levels.get(severity, 1) >= min_level:
                        f.write(f"<h2>{title}</h2>")
                        f.write(f"<pre>{content}</pre>")

                f.write("</body></html>")

            print("[+] HTML report saved as: pentest_report.html")
        except Exception as e:
            print(f"[!] Error saving HTML report: {str(e)}")
