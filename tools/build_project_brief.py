"""Create the visual one-page Mack project overview (2026-10-23 snapshot).

The accepted concept images are embedded unchanged. Requires ReportLab.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/mack-project-visual-brief.pdf"
INK = colors.HexColor("#213A49")
TEAL = colors.HexColor("#267A80")
MUTED = colors.HexColor("#536775")
AMBER = colors.HexColor("#A76529")
LINE = colors.HexColor("#CDD8DA")
PALE = colors.HexColor("#EEF4F3")
WHITE = colors.white


def build():
    fonts = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Brief", str(fonts / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("Brief-Bold", str(fonts / "Arial Bold.ttf")))
    pdfmetrics.registerFontFamily("Brief", normal="Brief", bold="Brief-Bold")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(612, 792), pageCompression=1)
    c.setTitle("Mack - Visual Project Brief")
    c.setAuthor("Mack project")
    c.setSubject("Personal AI companion: working desktop software and proposed robot body")

    def text(x, y, value, size=10, bold=False, color=INK):
        c.setFillColor(color)
        c.setFont("Brief-Bold" if bold else "Brief", size)
        c.drawString(x, y, value)

    def para(value, x, top, width, size=9, leading=11.5, color=MUTED):
        p = Paragraph(value, ParagraphStyle("body", fontName="Brief", fontSize=size,
                                           leading=leading, textColor=color))
        _, h = p.wrap(width, 790)
        p.drawOn(c, x, top - h)
        return top - h

    def line(x1, y1, x2, y2, color=LINE, width=0.7):
        c.setStrokeColor(color)
        c.setLineWidth(width)
        c.line(x1, y1, x2, y2)

    def icon(kind, x, y):
        c.saveState()
        c.setStrokeColor(TEAL)
        c.setFillColor(TEAL)
        c.setLineWidth(1.6)
        if kind == "speech":
            c.roundRect(x, y + 4, 23, 16, 4, fill=0, stroke=1)
            p = c.beginPath(); p.moveTo(x+5,y+4); p.lineTo(x+5,y); p.lineTo(x+10,y+4)
            c.drawPath(p)
            for dx in (6, 11.5, 17): c.circle(x+dx, y+12, 0.9, fill=1, stroke=0)
        elif kind == "memory":
            c.roundRect(x+2,y+1,18,21,2,fill=0,stroke=1)
            c.line(x+6,y+16,x+16,y+16); c.line(x+6,y+11,x+16,y+11); c.line(x+6,y+6,x+13,y+6)
        elif kind == "face":
            c.roundRect(x,y+4,23,17,3,fill=0,stroke=1)
            c.line(x+7,y+1,x+16,y+1); c.line(x+11.5,y+1,x+11.5,y+4)
            for dx in (8,15): c.circle(x+dx,y+14,0.9,fill=1,stroke=0)
            c.line(x+8,y+9,x+15,y+9)
        elif kind == "legs":
            c.roundRect(x+4,y+13,16,7,2,fill=0,stroke=1)
            for sign in (-1,1):
                start=x+12+sign*7
                p=c.beginPath();p.moveTo(start,y+13);p.lineTo(start+sign*4,y+7);p.lineTo(start,y+1);c.drawPath(p)
                c.circle(start+sign*4,y+7,1.4,fill=1,stroke=0)
        c.restoreState()

    text(36, 738, "MACK", 43, True)
    text(38, 718, "M.A.C. Model 04  /  Mobile Autonomous Computer", 9.2, color=MUTED)
    text(421, 771, "PROJECT BRIEF  /  23 OCT 2026", 7.7, True, MUTED)
    para("A personal AI companion<br/>in a familiar little Mac body.",
         321, 753, 255, 15, 18, INK)

    # The accepted appearance reference remains an unchanged raster inside the PDF.
    c.drawImage(str(ROOT / "concepts/raycue-build-target.png"),
                36, 345, width=540, height=360, preserveAspectRatio=True, mask="auto")
    c.setFillColor(WHITE)
    c.roundRect(48, 357, 181, 48, 3, fill=1, stroke=0)
    text(58, 393, "DONOR CLOCK / CATALOG [1]", 7.1, True, MUTED)
    text(58, 377, "80 x 91 x 112 mm", 12.2, True)
    text(58, 365, "229 g complete clock; robot mass TBD", 7.9, color=MUTED)
    text(36, 334, "AI-generated appearance concepts. The physical robot and dock have not been built.", 8, color=MUTED)

    # Four visual pillars, each with a concise, explicitly scoped description.
    features = [
        (36, "speech", "Talk", "Local conversation<br/>and an approved voice."),
        (174, "memory", "Remember", "Saved facts, history<br/>and familiar personality."),
        (312, "face", "See + express", "Classic desktop face;<br/>hidden camera planned."),
        (450, "legs", "Move", "4 legs / 12 axes proposed;<br/>self-righting is a goal."),
    ]
    for x, symbol, label, detail in features:
        icon(symbol, x, 296)
        text(x + 31, 303, label, 10.3, True)
        end = para(detail, x, 288, 126, 8.7, 11.5)
        assert end >= 260
    line(36, 252, 576, 252)

    text(36, 236, "FROM SOFTWARE TO A PHYSICAL COMPANION", 9.4, True, TEAL)
    line(44, 213, 44, 119, LINE, 1.2)
    steps = [
        (218, TEAL, "WORKING ON THE DEVELOPMENT MAC", "Classic desktop, local AI, spoken interaction<br/>and durable memory."),
        (171, AMBER, "ENGINEERING THE BODY", "Fit joints, onboard compute, vision and power.<br/>Plan local control for movement and stopping."),
        (124, INK, "NEXT: PROVE ONE COMPLETE LEG", "Resolve knee-motor placement, bearings and cables.<br/>Test under load before building the four-leg base."),
    ]
    for i, (y, color, heading, detail) in enumerate(steps, 1):
        c.setFillColor(color); c.circle(44, y-3, 7, fill=1, stroke=0)
        text(41.6, y-5.8, str(i), 8, True, WHITE)
        text(59, y, heading, 8.8, True, color)
        end = para(detail, 59, y-8, 320, 8.6, 11.3)
        assert end >= 91

    text(402, 236, "PLANNED HOME DOCK", 9.4, True, TEAL)
    c.drawImage(str(ROOT / "concepts/mack-charging-dock-v1.png"),
                402, 106, width=174, height=116, preserveAspectRatio=True, mask="auto")
    end = para("Lithium-ion power. Return, align<br/>and recharge autonomously.<br/><b>Concept; controls still to build.</b>",
               402, 100, 174, 8.3, 10.5)
    assert end >= 68

    c.setFillColor(PALE); c.roundRect(36, 34, 540, 28, 3, fill=1, stroke=0)
    text(46, 51, "LONG-TERM DIRECTION", 7.1, True, TEAL)
    text(46, 39, "Carry the same identity and memories into a future humanoid body, years from now.", 8.7)

    text(36, 21, "Build record: github.com/Bill-Viking/mack-model-04", 7.1, color=MUTED)
    c.linkURL("https://github.com/Bill-Viking/mack-model-04",(36,18,300,29),relative=0,thickness=0)
    text(344, 21, "[1] raycue.com/products/maclock  |  Catalog, not measured", 6.6, color=MUTED)
    c.linkURL("https://www.raycue.com/products/maclock",(344,18,576,29),relative=0,thickness=0)
    c.showPage(); c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
