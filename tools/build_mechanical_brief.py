"""Build Mack's one-page coworker review brief from the recorded design study.

Run with the Codex bundled Python (ReportLab and pypdf). No network access.
Output is a concept-review handout, not a drawing or manufacturing release.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/mack-mechanical-review-brief.pdf"
INK = colors.HexColor("#20323F")
MUTED = colors.HexColor("#52616A")
ACCENT = colors.HexColor("#246775")
PALE = colors.HexColor("#EFF4F5")
LINE = colors.HexColor("#CBD5DA")
WHITE = colors.white


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(612, 792), pageCompression=1)
    c.setTitle("Mack - Mechanical Design Review Brief")
    c.setAuthor("Mack project")
    c.setSubject("One-page concept review: compact quadruped joints and knee drive placement")

    def text(x, y, value, size=10, bold=False, color=INK):
        c.setFillColor(color)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, value)

    def para(value, x, top, width, size=10, leading=13, color=INK):
        style = ParagraphStyle("body", fontName="Helvetica", fontSize=size,
                               leading=leading, textColor=color, spaceAfter=0)
        p = Paragraph(value, style)
        _, h = p.wrap(width, 780)
        p.drawOn(c, x, top - h)
        return top - h

    def section(y, title):
        text(40, y, title, 11, True, ACCENT)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(40, y - 7, 572, y - 7)

    text(40, 752, "M.A.C. MODEL 04 / MACK", 9, True, ACCENT)
    text(410, 752, "22 OCT 2026  |  REV 1", 8.5, color=MUTED)
    text(40, 723, "Mechanical design review", 23, True)
    text(40, 704, "A compact four-legged robot in a retro Macintosh-shaped clock body", 10.5)
    end = para(
        "<b>Review goal:</b> Find a practical joint arrangement that preserves Mack's short-leg "
        "appearance. Resolve leg mechanics before docking controls. This is an early concept; "
        "no fitted complete leg or physical prototype exists yet.",
        40, 686, 532, 10, 13)
    assert end >= 644

    c.setFillColor(PALE)
    c.rect(40, 591, 532, 43, fill=1, stroke=0)
    for x, label, value in [
        (51, "DONOR BODY / CATALOG [1]", "80 x 91 x 112 mm"),
        (239, "DONOR CLOCK / CATALOG [1]", "229 g  /  8.08 oz"),
        (431, "PROPOSED LEG ACTUATION", "3 axes x 4 legs = 12"),
    ]:
        text(x, 620, label, 7.4, True, MUTED)
        text(x, 601, value, 12, True)
    para("Working W x D x H order is provisional. Actual interior, retained shell mass and completed robot mass are unknown.",
         40, 583, 532, 8.3, 10.5, MUTED)

    section(559, "PROPOSED JOINT CHAIN")
    # Schematic only: numbers identify rotations, not fabricated component sizes.
    c.setFillColor(PALE)
    c.roundRect(63, 505, 110, 32, 4, fill=1, stroke=0)
    text(76, 517, "Structural cradle", 10, True)
    p0, p1, p2, p3 = (118, 490), (148, 490), (177, 452), (148, 414)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(3)
    c.line(118, 505, *p0)
    for a, b in zip([p0, p1, p2], [p1, p2, p3]):
        c.line(*a, *b)
    for number, (x, y) in enumerate([p0, p1, p2], start=1):
        c.setFillColor(WHITE)
        c.setLineWidth(1.5)
        c.circle(x, y, 8, fill=1, stroke=1)
        text(x - 2.8, y - 3.4, str(number), 10, True, ACCENT)
    c.setFillColor(INK)
    c.ellipse(134, 407, 162, 418, fill=1, stroke=0)
    text(183, 474, "30 mm*", 8.7, color=MUTED)
    text(183, 430, "30 mm*", 8.7, color=MUTED)
    text(48, 421, "Passive foot", 8.7, color=MUTED)
    text(50, 391, "Schematic. *Proposed axis-to-axis link lengths.", 7.8, color=MUTED)

    y = 544
    for item in [
        "<b>1  Hip spread:</b> moves the leg sideways on a fore/aft axis.",
        "<b>2  Hip swing:</b> moves the upper leg forward/back on a transverse axis.",
        "<b>3  Knee:</b> bends the lower leg; parallel to the hip-swing axis.",
    ]:
        y = para(item, 278, y, 294, 9.6, 12.5) - 7
    y = para("<b>Load path:</b> foot, links, supported shafts and bearings, then cradle. "
             "The cosmetic shell and motor horn alone must not carry leg loads.",
             278, y, 294, 9.6, 12.5) - 7
    y = para("Retain a compliant foot with limited passive tilt. Allow space for "
             "stops, cable loops, bearing retention and service access.",
             278, y, 294, 9.2, 12)
    assert y >= 388

    section(372, "MAIN DECISION: WHERE DOES THE KNEE MOTOR GO?")
    for x, title, copy in [
        (40, "A / Motor at the knee", "First prototype baseline. Short drive path and fewer transmission parts; "
         "adds moving mass and bulk to the upper leg."),
        (314, "B / Motor beside the hip", "Belt or linkage drives the knee. Moves motor mass inward; adds routing, "
         "supports, tensioning and possible motion coupling."),
    ]:
        text(x, 348, title, 10, True)
        end = para(copy, x, 337, 258, 9.4, 12)
        assert end >= 287
    end = para(
        "<b>Scale check [2]:</b> A ROBOTIS XL330-M288-T case is 20 x 34 x 26 mm and 18 g. "
        "Twelve bare actuators total 216 g. Its 34 mm case dimension is already larger than our "
        "30 mm link pitch. This is a size benchmark, not a selected or load-qualified motor; "
        "published stall torque is not continuous capacity.",
        40, 278, 532, 9.3, 12)
    assert end >= 228

    section(213, "FEEDBACK REQUESTED")
    questions = [
        "Which knee-drive layout best fits this scale without losing the short-leg appearance?",
        "What bearing, shaft and cradle arrangement would you use to carry side loads and impacts?",
        "What assembled mass, joint torque and duty-cycle assumptions should govern motor selection?",
        "What would you change before building one leg? Self-righting reach is still unproven.",
    ]
    y = 195
    for i, question in enumerate(questions, 1):
        y = para(f"<b>{i}.</b> {question}", 40, y, 532, 9.5, 12) - 5
    assert y >= 121

    c.setFillColor(PALE)
    c.rect(40, 78, 532, 37, fill=1, stroke=0)
    end = para("<b>Next proof:</b> Verify the underside geometry and retained mass; fit real motor, "
               "bearing and cable envelopes into one leg; then test that leg in a restrained fixture "
               "under representative loads.", 50, 107, 512, 9.1, 11.5)
    assert end >= 80

    text(40, 63, "Sources checked 22 Oct 2026. Proposals are Mack design-study assumptions.", 7.5, color=MUTED)
    for y, label, url in [
        (51, "[1] RayCue WB-8: raycue.com/products/maclock", "https://www.raycue.com/products/maclock"),
        (39, "[2] ROBOTIS: emanual.robotis.com/docs/en/dxl/x/xl330-m288/", "https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/"),
    ]:
        text(40, y, label, 7.5, color=MUTED)
        c.linkURL(url, (40, y - 2, 450, y + 9), relative=0, thickness=0)
    text(539, 39, "1 / 1", 8, color=MUTED)
    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
