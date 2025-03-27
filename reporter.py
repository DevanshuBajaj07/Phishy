# reporter.py
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
import os

TXT_REPORT = "pentest_report.txt"
PDF_REPORT = "pentest_report.pdf"

class Reporter:
    def __init__(self):
        self.sections = []
        self.clear_reports()

    def clear_reports(self):
        open(TXT_REPORT, "w").close()
        if os.path.exists(PDF_REPORT):
            os.remove(PDF_REPORT)
        self.sections.clear()

    def add_section(self, title, content):
        self.sections.append((title, content))
        with open(TXT_REPORT, "a") as f:
            f.write(f"\n## {title} ##\n{content}\n")

    def finalize(self):
        self.generate_pdf_report()
        print(f"\n[+] Reports saved to:\n - {TXT_REPORT}\n - {PDF_REPORT}")

    def generate_pdf_report(self):
        c = canvas.Canvas(PDF_REPORT, pagesize=letter)
        width, height = letter
        margin = 40
        y = height - margin
        line_height = 14
        max_width = width - 2 * margin

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
