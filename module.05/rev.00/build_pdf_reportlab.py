from __future__ import annotations
import os
import textwrap
from datetime import datetime

# Open-source PDF generation with ReportLab
try:
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
except Exception as e:
    # Provide a clear message if reportlab isn't installed
    raise SystemExit("ReportLab is required. Install with: pip install reportlab\nError: " + str(e))

ROOT = os.path.dirname(__file__)
PLOTS_DIR = os.path.join(ROOT, "plots")
MOD2_PLOTS = os.path.normpath(os.path.join(ROOT, "..", "module.02", "plots"))
SQL_SUMMARY_MD = os.path.normpath(os.path.join(ROOT, "..", "module.02", "spacex_eda_sql_summary.md"))
FOLIUM_SCREENSHOT = os.path.normpath(os.path.join(ROOT, "..", "module.03", "folium_map.png"))
OUT_PDF = os.path.join(ROOT, "SpaceX_Capstone_OpenSource.pdf")

styles = getSampleStyleSheet()
style_title = styles['Title']
style_title.alignment = TA_CENTER
style_h1 = styles['Heading1']
style_h2 = styles['Heading2']
style_body = styles['BodyText']


def add_image_if_exists(flow, path: str, max_w=9.0*inch, max_h=5.0*inch):
    if os.path.exists(path):
        img = Image(path)
        # scale to fit
        w, h = img.wrap(0, 0)
        scale = min(max_w / w, max_h / h)
        img._restrictSize(max_w, max_h)
        img.drawWidth = w * scale
        img.drawHeight = h * scale
        flow.append(img)
        flow.append(Spacer(1, 0.2*inch))
        return True
    return False


def read_sql_summary() -> str:
    if os.path.exists(SQL_SUMMARY_MD):
        with open(SQL_SUMMARY_MD, 'r', encoding='utf-8') as f:
            return f.read()
    return "SQL EDA summary not found."


def build_pdf(metrics: dict | None = None) -> str:
    doc = SimpleDocTemplate(OUT_PDF, pagesize=landscape(letter), leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
    flow = []

    today = datetime.now().strftime('%Y-%m-%d')

    # Title
    flow.append(Paragraph("SpaceX Falcon 9 Launch Analysis", style_title))
    flow.append(Paragraph(f"Omar Essam — {today}", style_body))
    flow.append(Spacer(1, 0.4*inch))

    # Executive Summary
    flow.append(Paragraph("Executive Summary", style_h1))
    summary = """
    We analyzed SpaceX Falcon 9 launches to understand drivers of landing success and to build
    interactive analytics. We integrated CSV/API data, performed EDA and SQL analysis, constructed
    Folium and Plotly Dash visualizations, and trained baseline models. Key signals include payload
    mass ranges and booster version category.
    """
    flow.append(Paragraph(textwrap.fill(summary, 160), style_body))
    flow.append(PageBreak())

    # Introduction
    flow.append(Paragraph("Introduction", style_h1))
    intro = """
    Objective: predict first stage landing success and explore trends across launch sites. The dataset
    is sourced from the Skills Network SpaceX CSV with a local merged variant for robustness. Tools
    include pandas, SQLite, seaborn/matplotlib, Plotly, Folium, and Dash.
    """
    flow.append(Paragraph(textwrap.fill(intro, 160), style_body))
    flow.append(PageBreak())

    # Data Collection & Wrangling
    flow.append(Paragraph("Data Collection & Wrangling", style_h1))
    dcw = """
    Data was collected from a public CSV and enriched locally. We standardized column names and types,
    engineered features such as landing success (class), booster version category, and ensured geospatial
    coordinates. Missing values were handled and types coerced.
    """
    flow.append(Paragraph(textwrap.fill(dcw, 160), style_body))
    flow.append(PageBreak())

    # EDA & Interactive Methodology
    flow.append(Paragraph("EDA & Interactive Visual Analytics Methodology", style_h1))
    meth = """
    We inspected distributions, yearly trends, and relationships, then built interactive analytics:
    Folium map for spatial patterns and Plotly Dash for payload vs. success with site filters. The app
    includes a pie chart of success by site and a payload-success scatter.
    """
    flow.append(Paragraph(textwrap.fill(meth, 160), style_body))
    flow.append(PageBreak())

    # Visualization Results (Module 02 Plots)
    flow.append(Paragraph("EDA Results", style_h1))
    add_image_if_exists(flow, os.path.join(MOD2_PLOTS, 'outcomes_by_year.png'))
    add_image_if_exists(flow, os.path.join(MOD2_PLOTS, 'payload_distribution.png'))
    add_image_if_exists(flow, os.path.join(MOD2_PLOTS, 'top_launch_sites.png'))
    flow.append(PageBreak())

    # SQL Findings
    flow.append(Paragraph("EDA with SQL: Key Findings", style_h1))
    flow.append(Paragraph(textwrap.fill(read_sql_summary(), 160), style_body))
    flow.append(PageBreak())

    # Folium Map
    flow.append(Paragraph("Interactive Map (Folium)", style_h1))
    if not add_image_if_exists(flow, FOLIUM_SCREENSHOT):
        flow.append(Paragraph("Add screenshot at module.03/folium_map.png to include it here.", style_body))
    flow.append(PageBreak())

    # Dash Results
    flow.append(Paragraph("Dash Results", style_h1))
    add_image_if_exists(flow, os.path.join(PLOTS_DIR, 'dash_pie_success_by_site.png'))
    add_image_if_exists(flow, os.path.join(PLOTS_DIR, 'dash_scatter_payload_vs_success.png'))
    flow.append(PageBreak())

    # Predictive Methodology & Results
    flow.append(Paragraph("Predictive Analysis: Methodology", style_h1))
    flow.append(Paragraph(textwrap.fill("Split train/test, scale numeric features, encode categoricals, and evaluate multiple classifiers with tuning using accuracy and F1.", 160), style_body))
    flow.append(Spacer(1, 0.2*inch))
    flow.append(Paragraph("Predictive Analysis: Results", style_h1))
    metrics = metrics or {}
    best = metrics.get('best_model', 'TBD')
    acc = metrics.get('accuracy', 'TBD')
    f1 = metrics.get('f1', 'TBD')
    flow.append(Paragraph(textwrap.fill(f"Best model: {best}. Test accuracy: {acc}. Test F1: {f1}.", 160), style_body))
    flow.append(PageBreak())

    # Conclusion
    flow.append(Paragraph("Conclusion", style_h1))
    concl = """
    Payload mass and booster category are key success drivers. Interactive tools enable site-specific
    exploration. The baseline model offers a starting point; additional features and temporal effects
    can further improve performance.
    """
    flow.append(Paragraph(textwrap.fill(concl, 160), style_body))

    doc.build(flow)
    return OUT_PDF


if __name__ == '__main__':
    path = build_pdf()
    print(f"Saved open-source PDF to: {path}")
