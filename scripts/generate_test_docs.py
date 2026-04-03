"""
generate_test_docs.py
─────────────────────
Generates synthetic tax document PDFs for testing and development.

Produces:
  samples/sample_w2.pdf       — IRS Form W-2 (Wage and Tax Statement)
  samples/sample_1099_int.pdf — IRS Form 1099-INT (Interest Income)

All documents are clearly marked as synthetic test data.
No real taxpayer information is used or implied.

Requirements:
  pip install reportlab

Usage:
  python generate_test_docs.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

W, H = letter  # 612 x 792 points

OUTPUT_DIR = "samples"


# ─────────────────────────────────────────────────────────────────────────────
#  DRAWING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def draw_box(c, x, y, w, h):
    c.rect(x, y, w, h)


def draw_label(c, x, y, text, size=6.5, bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, text)


def draw_value(c, x, y, text, size=9):
    c.setFont("Helvetica", size)
    c.drawString(x, y, text)


def draw_section(c, x, y, w, h, title, title_size=6):
    """Draw a labeled box section."""
    draw_box(c, x, y, w, h)
    draw_label(c, x + 2, y + h - 9, title, size=title_size)


# ─────────────────────────────────────────────────────────────────────────────
#  W-2  —  Wage and Tax Statement (2025)
#  Employee: Robert B. Chen  |  Employer: Brightline Solutions LLC (TX)
#  Key values: Wages $72,500 | Fed withheld $11,200 | SIMPLE IRA Code E
# ─────────────────────────────────────────────────────────────────────────────

def make_w2(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)

    # ── Title bar ──────────────────────────────────────────────────────────
    c.setFillColorRGB(0.18, 0.31, 0.53)
    c.rect(36, 730, 540, 30, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(42, 740, "Form W-2   Wage and Tax Statement   2025   Copy B")
    c.setFont("Helvetica", 7)
    c.drawString(360, 740, "Department of the Treasury — Internal Revenue Service")
    c.setFillColor(colors.black)

    rh = 36  # standard row height

    # ── Row 1: SSN | OMB | Box 1 | Box 2 ──────────────────────────────────
    y = 700
    draw_section(c, 36,  y, 160, rh, "a  Employee's social security number")
    draw_value(c, 44, y + 12, "456-78-9012")

    draw_section(c, 196, y, 100, rh, "OMB No. 1545-0029")
    draw_value(c, 202, y + 12, "1545-0029", size=8)

    draw_section(c, 296, y, 140, rh, "1  Wages, tips, other compensation")
    draw_value(c, 304, y + 12, "72,500.00")

    draw_section(c, 436, y, 140, rh, "2  Federal income tax withheld")
    draw_value(c, 444, y + 12, "11,200.00")

    # ── Row 2: Employer | Box 3 | Box 4 ───────────────────────────────────
    y -= rh
    draw_section(c, 36,  y, 260, rh, "c  Employer's name, address, and ZIP code")
    draw_value(c, 44, y + 20, "Brightline Solutions LLC")
    draw_value(c, 44, y + 10, "789 Commerce Blvd, Austin, TX 78701", size=8)

    draw_section(c, 296, y, 140, rh, "3  Social security wages")
    draw_value(c, 304, y + 12, "72,500.00")

    draw_section(c, 436, y, 140, rh, "4  Social security tax withheld")
    draw_value(c, 444, y + 12, "4,495.00")

    # ── Row 3: EIN | Control | Box 5 | Box 6 ──────────────────────────────
    y -= rh
    draw_section(c, 36,  y, 130, rh, "b  Employer identification number (EIN)")
    draw_value(c, 44, y + 12, "45-6789012")

    draw_section(c, 166, y, 130, rh, "d  Control number")
    draw_value(c, 174, y + 12, "X9Y8Z7")

    draw_section(c, 296, y, 140, rh, "5  Medicare wages and tips")
    draw_value(c, 304, y + 12, "72,500.00")

    draw_section(c, 436, y, 140, rh, "6  Medicare tax withheld")
    draw_value(c, 444, y + 12, "1,051.25")

    # ── Row 4: Employee name | Box 7 | Box 8 ──────────────────────────────
    y -= rh
    draw_section(c, 36,  y, 260, rh, "e  Employee's first name and initial  Last name")
    draw_value(c, 44, y + 20, "Robert B. Chen")

    draw_section(c, 296, y, 140, rh, "7  Social security tips")
    draw_value(c, 304, y + 12, "0.00")

    draw_section(c, 436, y, 140, rh, "8  Allocated tips")
    draw_value(c, 444, y + 12, "0.00")

    # ── Row 5: Address | Box 9 | Box 10 | Box 11 ──────────────────────────
    y -= rh
    draw_section(c, 36,  y, 260, rh, "f  Employee's address and ZIP code")
    draw_value(c, 44, y + 12, "221 Maple Ave, Austin, TX 78702")

    draw_section(c, 296, y, 70,  rh, "9")
    draw_value(c, 304, y + 12, "(blank)")

    draw_section(c, 366, y, 70,  rh, "10  Dependent care benefits")
    draw_value(c, 374, y + 12, "0.00")

    draw_section(c, 436, y, 140, rh, "11  Nonqualified plans")
    draw_value(c, 444, y + 12, "0.00")

    # ── Row 6: Box 12a | Box 12b | Box 13 | Box 14 ────────────────────────
    y -= rh
    draw_section(c, 36,  y, 130, rh, "12a  Code")
    draw_value(c, 44, y + 20, "Code: E")
    draw_value(c, 44, y + 10, "2,500.00", size=8)
    draw_label(c, 44, y + 2,  "SIMPLE IRA contribution", size=6)

    draw_section(c, 166, y, 130, rh, "12b  Code")
    draw_value(c, 174, y + 20, "Code: DD")
    draw_value(c, 174, y + 10, "6,200.00", size=8)
    draw_label(c, 174, y + 2,  "Employer health coverage", size=6)

    draw_section(c, 296, y, 140, rh, "13  Checkboxes")
    draw_value(c, 304, y + 20, "Statutory employee: No")
    draw_value(c, 304, y + 10, "Retirement plan: Yes")
    draw_value(c, 304, y + 2,  "Third-party sick pay: No", size=7)

    draw_section(c, 436, y, 140, rh, "14  Other")
    draw_value(c, 444, y + 12, "(none)")

    # ── Row 7: State boxes 15-19 ───────────────────────────────────────────
    y -= rh
    draw_section(c, 36,  y, 70,  rh, "15  State / Employer state ID")
    draw_value(c, 44, y + 20, "TX")
    draw_value(c, 44, y + 10, "45-6789012", size=7.5)

    draw_section(c, 106, y, 110, rh, "16  State wages, tips, etc.")
    draw_value(c, 114, y + 12, "72,500.00")

    draw_section(c, 216, y, 80,  rh, "17  State income tax")
    draw_value(c, 224, y + 12, "0.00")
    draw_label(c, 224, y + 2,   "TX has no state income tax", size=5.5)

    draw_section(c, 296, y, 140, rh, "18  Local wages, tips, etc.")
    draw_value(c, 304, y + 12, "72,500.00")

    draw_section(c, 436, y, 140, rh, "19  Local income tax")
    draw_value(c, 444, y + 12, "0.00")

    # ── Math verification note ─────────────────────────────────────────────
    y -= 22
    c.setFont("Helvetica", 6)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(36, y,
        "Verification: SS tax (Box 4) = 6.2% x $72,500 = $4,495.00 ✓   "
        "Medicare (Box 6) = 1.45% x $72,500 = $1,051.25 ✓")
    c.setFillColor(colors.black)

    # ── Footer ─────────────────────────────────────────────────────────────
    y -= 12
    c.setFont("Helvetica", 6.5)
    c.drawString(36, y,
        "THIS IS A SYNTHETIC TEST DOCUMENT — NOT A REAL W-2. "
        "FOR DEVELOPMENT AND TESTING PURPOSES ONLY.")
    c.drawString(36, y - 10,
        "Notice to Employee: Report wages on Form 1040 Line 1a. "
        "See IRS instructions for Schedule A (state tax) and Schedule SE.")

    c.save()
    print(f"  ✓  W-2 saved → {path}")


# ─────────────────────────────────────────────────────────────────────────────
#  1099-INT  —  Interest Income (2025)
#  Payer: Meridian Federal Bank  |  Recipient: Patricia M. Torres (IL)
#  Key values: Taxable interest $3,840 | Backup withholding $960 |
#              Tax-exempt interest $450 | Early withdrawal penalty $125
# ─────────────────────────────────────────────────────────────────────────────

def make_1099_int(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)

    # ── Title bar ──────────────────────────────────────────────────────────
    c.setFillColorRGB(0.18, 0.31, 0.53)
    c.rect(36, 730, 540, 30, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(42, 740, "Form 1099-INT   Interest Income   2025")
    c.setFont("Helvetica", 7)
    c.drawString(360, 740, "Department of the Treasury — Internal Revenue Service")
    c.setFillColor(colors.black)

    # ── Payer block ────────────────────────────────────────────────────────
    y = 700
    draw_section(c, 36,  y, 300, 50,
                 "PAYER'S name, street address, city, state, ZIP code, and telephone no.",
                 title_size=6.5)
    draw_value(c, 44, y + 35, "Meridian Federal Bank")
    draw_value(c, 44, y + 24, "500 Financial Plaza, Chicago, IL 60601", size=8)
    draw_value(c, 44, y + 14, "Phone: (312) 555-0199", size=8)

    draw_section(c, 336, y, 240, 50,
                 "OMB No. 1545-0112 / CORRECTED (if checked): No")
    draw_value(c, 344, y + 30, "PAYER'S TIN:  36-4567890")
    draw_value(c, 344, y + 20, "RECIPIENT'S TIN:  789-01-2345")
    draw_value(c, 344, y + 10, "Account number:  CHK-2025-8847", size=8)

    # ── Recipient block ────────────────────────────────────────────────────
    y -= 56
    draw_section(c, 36, y, 300, 44,
                 "RECIPIENT'S name, street address, city, state, and ZIP code")
    draw_value(c, 44, y + 30, "Patricia M. Torres")
    draw_value(c, 44, y + 20, "88 Lakeview Drive")
    draw_value(c, 44, y + 10, "Naperville, IL 60540")

    # ── Amount boxes ───────────────────────────────────────────────────────
    y  -= 50
    rh  = 38
    bw  = 180

    # Row A: Box 1 | Box 2 | Box 3
    draw_section(c, 36,  y, bw,  rh, "1  Interest income")
    draw_value(c, 44, y + 15, "3,840.00")
    draw_label(c, 44, y + 5,  "Taxable interest — savings/CD accounts", size=6)

    draw_section(c, 216, y, bw,  rh, "2  Early withdrawal penalty")
    draw_value(c, 224, y + 15, "125.00")
    draw_label(c, 224, y + 5,  "CD early withdrawal fee", size=6)

    draw_section(c, 396, y, 180, rh,
                 "3  Interest on U.S. Savings Bonds / Treasury obligations")
    draw_value(c, 404, y + 15, "0.00")

    # Row B: Box 4 | Box 5 | Box 6
    y -= rh
    draw_section(c, 36,  y, bw,  rh, "4  Federal income tax withheld")
    draw_value(c, 44, y + 15, "960.00")
    draw_label(c, 44, y + 5,  "Backup withholding applied", size=6)

    draw_section(c, 216, y, bw,  rh, "5  Investment expenses")
    draw_value(c, 224, y + 15, "0.00")

    draw_section(c, 396, y, 180, rh, "6  Foreign tax paid")
    draw_value(c, 404, y + 15, "0.00")

    # Row C: Box 7 | Box 8 | Box 9
    y -= rh
    draw_section(c, 36,  y, bw,  rh, "7  Foreign country or U.S. possession")
    draw_value(c, 44, y + 15, "N/A")

    draw_section(c, 216, y, bw,  rh, "8  Tax-exempt interest")
    draw_value(c, 224, y + 15, "450.00")
    draw_label(c, 224, y + 5,  "Municipal bond — not taxable federally", size=6)

    draw_section(c, 396, y, 180, rh,
                 "9  Specified private activity bond interest")
    draw_value(c, 404, y + 15, "0.00")

    # Row D: Box 10 | Box 11 | Box 12
    y -= rh
    draw_section(c, 36,  y, bw,  rh, "10  Market discount")
    draw_value(c, 44, y + 15, "0.00")

    draw_section(c, 216, y, bw,  rh, "11  Bond premium")
    draw_value(c, 224, y + 15, "0.00")

    draw_section(c, 396, y, 180, rh,
                 "12  Bond premium on Treasury obligations")
    draw_value(c, 404, y + 15, "0.00")

    # Row E: Box 13 | Box 14 | Box 15-16
    y -= rh
    draw_section(c, 36,  y, bw,  rh, "13  Bond premium on tax-exempt bond")
    draw_value(c, 44, y + 15, "0.00")

    draw_section(c, 216, y, bw,  rh,
                 "14  Tax-exempt / tax credit bond CUSIP no.")
    draw_value(c, 224, y + 15, "N/A")

    draw_section(c, 396, y, 180, rh, "15  State  /  16  State ID no.")
    draw_value(c, 404, y + 20, "IL")
    draw_value(c, 440, y + 20, "36-4567890")

    # Row F: Box 17
    y -= rh
    draw_section(c, 36, y, bw, rh, "17  State income tax withheld")
    draw_value(c, 44, y + 15, "192.00")
    draw_label(c, 44, y + 5,  "Illinois state withholding", size=6)

    # ── Key mapping summary box ────────────────────────────────────────────
    y -= 52
    c.setFillColorRGB(0.94, 0.96, 0.99)
    c.rect(36, y, 540, 42, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(44, y + 30, "FORM 1040 MAPPING REFERENCE:")
    c.setFont("Helvetica", 7.5)
    c.drawString(44, y + 20,
        "Box 1  Taxable Interest ($3,840)     →  Schedule B Part I  →  Form 1040 Line 2b"
        "  [Schedule B required: amount > $1,500]")
    c.drawString(44, y + 11,
        "Box 2  Early Withdrawal ($125)       →  Schedule 1 Line 18 "
        "(above-the-line deduction, reduces AGI)")
    c.drawString(44, y + 2,
        "Box 4  Fed Tax Withheld ($960)       →  Form 1040 Line 25b  "
        "|  Box 8  Tax-Exempt ($450)  →  Form 1040 Line 2a (informational)")

    # ── Footer ─────────────────────────────────────────────────────────────
    y -= 18
    c.setFont("Helvetica", 6.5)
    c.drawString(36, y,
        "THIS IS A SYNTHETIC TEST DOCUMENT — NOT A REAL 1099-INT. "
        "FOR DEVELOPMENT AND TESTING PURPOSES ONLY.")
    c.drawString(36, y - 10,
        "Copy B — For Recipient. "
        "Report interest income on Schedule B when total taxable interest exceeds $1,500.")

    c.save()
    print(f"  ✓  1099-INT saved → {path}")


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\nGenerating synthetic tax document PDFs...")
    print(f"Output directory: {OUTPUT_DIR}/\n")

    make_w2(os.path.join(OUTPUT_DIR, "sample_w2.pdf"))
    make_1099_int(os.path.join(OUTPUT_DIR, "sample_1099_int.pdf"))

    print("\nDone. Files generated:")
    print(f"  {OUTPUT_DIR}/sample_w2.pdf")
    print(f"  {OUTPUT_DIR}/sample_1099_int.pdf")
    print("\nNOTE: These are synthetic test documents only.")
    print("      No real taxpayer data is used or implied.")
