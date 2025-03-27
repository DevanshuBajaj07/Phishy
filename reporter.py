# reporter.py
# Handles saving of scan results to TXT and PDF reports.
# Reports can include multiple sections and are created in a user-friendly format.

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
import os

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
        - Generates the PDF version from all saved sections
        - Displays success message with file paths
        """
        self.generate_pdf_report()
        print(f"\n[+] Reports saved to:\n - {self.txt_filename}\n - {self.pdf_filename}")

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
                # New page if near bottom
                if y < margin + 2 * line_height:
                    c.showPage()
                    y = height - margin

                # Section title
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, y, title)
                underline_width = stringWidth(title, "Helvetica-Bold", 12)
                c.line(margin, y - 1, margin + underline_width, y - 1)
                y -= line_height

                # Section content with word wrap
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
