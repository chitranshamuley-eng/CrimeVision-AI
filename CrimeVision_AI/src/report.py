from io import BytesIO
from datetime import datetime, timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

DISCLAIMER = "PROTOTYPE / HUMAN REVIEW REQUIRED. Machine-generated observations are not verified forensic conclusions. Do not use this report alone to identify a suspect, determine guilt, or make legal conclusions."

def _safe(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\\n"," ")

def generate_pdf_report(case_label, timeline, image_results=None, audio_results=None, video_results=None):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=14*mm, leftMargin=14*mm, topMargin=14*mm, bottomMargin=14*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph("CrimeVision AI — Evidence Review Report", styles["Title"]), Spacer(1, 5*mm),
        Paragraph("<b>Case label:</b> "+_safe(case_label), styles["BodyText"]),
        Paragraph("<b>Generated UTC:</b> "+datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), styles["BodyText"]),
        Spacer(1, 3*mm), Paragraph("<b>"+_safe(DISCLAIMER)+"</b>", styles["BodyText"]), Spacer(1, 4*mm),
        Paragraph("Processing summary", styles["Heading2"]),
        Paragraph(f"Image files: {len(image_results or [])}; audio files: {len(audio_results or [])}; video files: {len(video_results or [])}.", styles["BodyText"]),
        Spacer(1, 3*mm), Paragraph("Chronological observations", styles["Heading2"])]
    rows = [["Time", "Modality", "Source", "Observation"]]
    for e in timeline[:400]:
        rows.append([_safe(e.get("time_label","Time unknown")), _safe(e.get("modality","")),
                     _safe(e.get("source",""))[:80], _safe(e.get("event",""))[:500]])
    if len(rows) == 1: rows.append(["—","—","—","No observations recorded"])
    table = Table(rows, repeatRows=1, colWidths=[23*mm, 19*mm, 34*mm, 100*mm])
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#183153")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.3,colors.grey),
        ("FONTSIZE",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story.extend([table, Spacer(1, 4*mm), Paragraph("Review checklist", styles["Heading2"])])
    for item in ["Compare labels and transcripts against original evidence.",
                 "Document reviewer, date, corrections, time zone, and discrepancies.",
                 "Preserve original files and maintain chain-of-custody records outside this prototype.",
                 "A missing detection is not proof that an object or event was absent.",
                 "The prototype samples video frames and does not perform validated action recognition."]:
        story.append(Paragraph("• "+_safe(item), styles["BodyText"]))
    doc.build(story)
    return buf.getvalue()
