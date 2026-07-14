"""
Feature 8: Final Report Generator
Tổng hợp dataset overview, scraping method, extracted data summary,
analysis results, charts, key findings, limitations và conclusion
thành 1 file PDF duy nhất: output/final_report.pdf
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Giải quyết triệt để vấn đề đường dẫn (giống các module khác trong src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"

SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"
ANALYSIS_JSON = OUTPUT_DIR / "analysis_results.json"

FINAL_REPORT_PDF = OUTPUT_DIR / "final_report.pdf"

CHART_FILES = {
    "word_count_by_section": ("Top 10 Sections by Word Count",
                              CHARTS_DIR / "word_count_by_section.png"),
    "code_examples_by_section": ("Number of Code Examples by Section",
                                 CHARTS_DIR / "code_examples_by_section.png"),
    "link_type_distribution": ("Link Type Distribution",
                               CHARTS_DIR / "link_type_distribution.png"),
    "code_linecount_hist": ("Code Example Line Count Distribution",
                            CHARTS_DIR / "code_linecount_hist.png"),
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _load_analysis_results() -> Dict:
    with open(ANALYSIS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_row_counts() -> Dict[str, int]:
    sections_df = pd.read_csv(SECTIONS_CSV, encoding="utf-8-sig")
    links_df = pd.read_csv(LINKS_CSV, encoding="utf-8-sig")
    code_examples_df = pd.read_csv(CODE_EXAMPLES_CSV, encoding="utf-8-sig")
    return {
        "sections": len(sections_df),
        "links": len(links_df),
        "code_examples": len(code_examples_df),
    }


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle", parent=styles["Title"], fontSize=22, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle", parent=styles["Normal"], fontSize=11,
        textColor=colors.grey, spaceAfter=24,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading", parent=styles["Heading1"], fontSize=15,
        spaceBefore=18, spaceAfter=10, textColor=colors.HexColor("#2C3E50"),
    ))
    styles.add(ParagraphStyle(
        name="BodyJustified", parent=styles["Normal"], fontSize=10.5,
        leading=15, alignment=4,  # 4 = justify
    ))
    styles.add(ParagraphStyle(
        name="TableText", parent=styles["Normal"], fontSize=9, leading=12
    ))
    styles.add(ParagraphStyle(
        name="TableHeader", parent=styles["Normal"], fontSize=9, leading=12, textColor=colors.white, fontName="Helvetica-Bold"
    ))
    return styles


# --------------------------------------------------------------------------
# Section builders (mỗi hàm trả về list Flowable để append vào story)
# --------------------------------------------------------------------------

def _section_cover(styles, row_counts: Dict) -> list:
    story = [
        Spacer(1, 4 * cm),
        Paragraph("BeautifulSoup Documentation Analytics System", styles["ReportTitle"]),
        Paragraph(
            "Final Analytical Report — Collect · Parse · Extract · Analyze · Visualize",
            styles["ReportSubtitle"],
        ),
        Spacer(1, 1 * cm),
        Paragraph(
            f"Sections extracted: {row_counts['sections']} &nbsp;|&nbsp; "
            f"Links extracted: {row_counts['links']} &nbsp;|&nbsp; "
            f"Code examples extracted: {row_counts['code_examples']}",
            styles["Normal"],
        ),
        PageBreak(),
    ]
    return story


def _section_dataset_overview(styles, row_counts: Dict) -> list:
    story = [
        Paragraph("1. Dataset Overview", styles["SectionHeading"]),
        Paragraph(
            "The dataset was built from a single technical documentation page: the "
            "official Beautiful Soup 4 documentation "
            "(https://www.crummy.com/software/BeautifulSoup/bs4/doc/). "
            "The page was downloaded once, parsed, and broken down into three "
            "structured tables covering sections, hyperlinks, and Python code examples.",
            styles["BodyJustified"],
        ),
        Spacer(1, 0.3 * cm),
    ]
    raw_table_data = [
        ["Dataset", "Rows", "Description"],
        ["sections.csv", str(row_counts["sections"]), "Headings (h1/h2/h3) with text, word count, code block count, link count"],
        ["links.csv", str(row_counts["links"]), "All hyperlinks with text, href, type, and originating section"],
        ["code_examples.csv", str(row_counts["code_examples"]), "Python code blocks with line count and BS4-method usage flags"],
    ]
    table_data = []
    table_data.append([Paragraph(cell, styles["TableHeader"]) for cell in raw_table_data[0]])
    for row in raw_table_data[1:]:
        table_data.append([Paragraph(cell, styles["TableText"]) for cell in row])

    t = Table(table_data, colWidths=[3.5 * cm, 2.0 * cm, 10.5 * cm], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F6F7")]),
    ]))
    story.append(t)
    return story


def _section_scraping_method(styles) -> list:
    bullets = [
        "requests was used to send an HTTP GET request to the target URL and verify the HTTP status code before saving.",
        "The raw HTML response was saved to data/raw/beautifulsoup_doc.html for reproducibility.",
        "BeautifulSoup parsed the saved HTML using Python's built-in html.parser. The official documentation also describes lxml as a faster alternative and html5lib as a more lenient but slower alternative.",
        "Sections were identified via h1/h2/h3 headings; text between one heading and the next was assigned to that section.",
        "Links were extracted by iterating over soup.find_all('a') and reading each href attribute, then classified into 5 categories.",
        "Code examples were extracted from <pre> tags and analyzed for the presence of key BeautifulSoup methods (find_all, find, select, get_text) and the requests library.",
    ]
    story = [
        Paragraph("2. Scraping Method", styles["SectionHeading"]),
        ListFlowable(
            [ListItem(Paragraph(b, styles["BodyJustified"])) for b in bullets],
            bulletType="bullet",
        ),
    ]
    return story


def _section_extracted_data_summary(styles, results: Dict) -> list:
    story = [
        Paragraph("3. Extracted Data Summary", styles["SectionHeading"]),
        Paragraph(
            f"A total of {results['q1_total_sections']} documentation sections were "
            f"identified. The longest section by word count is "
            f"\u201c{results['q2_highest_word_count_section']['section_title']}\u201d "
            f"with {results['q2_highest_word_count_section']['word_count']} words. "
            f"Link classification found "
            f"{results['q6_internal_external_links']['internal_anchor']} internal anchors "
            f"and {results['q6_internal_external_links']['external_link']} external links, "
            f"among other link types recorded in links.csv.",
            styles["BodyJustified"],
        ),
    ]
    return story


def _section_analysis_results(styles, results: Dict) -> list:
    raw_rows = [
        ["#", "Question", "Answer"],
        ["Q1", "How many sections are in the documentation?",
         str(results["q1_total_sections"])],
        ["Q2", "Which section has the highest word count?",
         f'{results["q2_highest_word_count_section"]["section_title"]} '
         f'({results["q2_highest_word_count_section"]["word_count"]} words)'],
        ["Q3", "Which section contains the most code examples?",
         f'{results["q3_most_code_examples_section"]["section_title"]} '
         f'({results["q3_most_code_examples_section"]["code_block_count"]})'],
        ["Q4", "Which section contains the most links?",
         f'{results["q4_most_links_section"]["section_title"]} '
         f'({results["q4_most_links_section"]["link_count"]})'],
        ["Q5", "Top 10 most frequent technical keywords",
         ", ".join(k["keyword"] for k in results["q5_top10_keywords"][:10])],
        ["Q6", "Internal vs. external links",
         f'internal: {results["q6_internal_external_links"]["internal_anchor"]}, '
         f'external: {results["q6_internal_external_links"]["external_link"]}'],
        ["Q7", "Code examples using find_all()", str(results["q7_find_all_usage"])],
        ["Q8", "Code examples using get_text()", str(results["q8_get_text_usage"])],
        ["Q9*", "Word count statistics (mean / median / std)",
         f'{results["q9_word_count_statistics"]["mean"]:.1f} / '
         f'{results["q9_word_count_statistics"]["median"]:.1f} / '
         f'{results["q9_word_count_statistics"]["std"]:.1f}'],
        ["Q10*", "% of code examples using a BS4 search method",
         f'{results["q10_bs4_method_usage_ratio"]["percentage"]}%'],
    ]
    rows = []
    rows.append([Paragraph(cell, styles["TableHeader"]) for cell in raw_rows[0]])
    for r in raw_rows[1:]:
        rows.append([Paragraph(cell, styles["TableText"]) for cell in r])

    t = Table(rows, colWidths=[1.2 * cm, 7.3 * cm, 7.5 * cm], repeatRows=1, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F6F7")]),
    ]))
    story = [
        Paragraph("4. Analysis Results", styles["SectionHeading"]),
        Paragraph("(* = additional question proposed by the team)", styles["Normal"]),
        Spacer(1, 0.2 * cm),
        t,
    ]
    return story


def _section_charts(styles) -> list:
    story = [Paragraph("5. Charts", styles["SectionHeading"])]
    for title, path in CHART_FILES.values():
        if path.exists():
            story.append(KeepTogether([
                Paragraph(title, styles["Heading3"]),
                Image(str(path), width=14.5 * cm, height=8.2 * cm, kind="proportional"),
                Spacer(1, 0.4 * cm),
            ]))
        else:
            story.append(Paragraph(f"[Missing chart: {path.name}]", styles["Normal"]))
    return story


def _section_key_findings(styles, results: Dict, row_counts: Dict) -> list:
    bullets = [
        f'The section \u201c{results["q2_highest_word_count_section"]["section_title"]}\u201d is the most '
        f'content-heavy part of the documentation, suggesting it is a core reference area for users.',
        f'The majority of links ({results["q6_internal_external_links"]["internal_anchor"]} out of '
        f'{row_counts["links"]}) are internal anchors, meaning the documentation is largely self-contained and '
        f'relies on in-page navigation rather than external references.',
        f'Only {results["q7_find_all_usage"]} code examples explicitly use find_all(), while '
        f'{results["q10_bs4_method_usage_ratio"]["percentage"]}% of all code examples use at least one '
        f'core search method (find_all/find/select), showing these methods are central but not universal '
        f'across all examples.',
        f'get_text() appears in only {results["q8_get_text_usage"]} code examples, indicating it is a '
        f'less emphasized method compared to element search methods.',
        f'Section word counts vary widely (std \u2248 {results["q9_word_count_statistics"]["std"]:.0f} words), '
        f'reflecting a mix of short reference sections and long explanatory ones.',
    ]
    story = [
        Paragraph("6. Key Findings", styles["SectionHeading"]),
        ListFlowable(
            [ListItem(Paragraph(b, styles["BodyJustified"])) for b in bullets],
            bulletType="bullet",
        ),
    ]
    return story


def _section_limitations(styles) -> list:
    bullets = [
        "The analysis is based on a single snapshot of the documentation page; results will change if the page is updated.",
        "Keyword extraction uses a simple tokenizer and a minimal stopword list, so some non-technical words may still appear in the top-10 list.",
        "Sections are delimited purely by heading tags (h1/h2/h3); pages with inconsistent heading structure could lead to mis-assigned content.",
        "Link classification relies on hostname matching for 'documentation_link' vs 'external_link', which may misclassify uncommon URL formats.",
        "The system currently analyzes only one documentation page; it has not been tested for scale across multiple pages or sites.",
    ]
    story = [
        Paragraph("7. Limitations", styles["SectionHeading"]),
        ListFlowable(
            [ListItem(Paragraph(b, styles["BodyJustified"])) for b in bullets],
            bulletType="bullet",
        ),
    ]
    return story


def _section_conclusion(styles, results: Dict, row_counts: Dict) -> list:
    text = (
        f"This project successfully built an end-to-end pipeline that collects, parses, "
        f"extracts, analyzes, and visualizes the Beautiful Soup documentation. "
        f"Across {results['q1_total_sections']} sections, "
        f"{results['q10_bs4_method_usage_ratio']['total_code_examples']} code examples, and "
        f"{row_counts['links']} "
        f"classified links, the analysis shows a documentation page that is text-heavy, "
        f"strongly self-referential through internal anchors, and centered on a small set of "
        f"core BeautifulSoup search methods. The pipeline is modular (collector, parser, "
        f"extractor, analyzer, visualizer, report generator) and can be re-run end-to-end "
        f"whenever the source documentation changes."
    )
    return [
        Paragraph("8. Conclusion", styles["SectionHeading"]),
        Paragraph(text, styles["BodyJustified"]),
    ]


def _draw_page_number(canvas, doc) -> None:
    """Draw a compact footer on report pages."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 0.8 * cm, f"Page {doc.page}")
    canvas.restoreState()


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def run_report_generator(analysis_results: Optional[Dict] = None) -> Optional[str]:
    """
    Tạo output/final_report.pdf từ kết quả Feature 6 (analyzer) và
    biểu đồ Feature 7 (visualizer).

    analysis_results: dict trả về từ run_all_analytics() (Feature 6).
                       Nếu None, tự đọc lại từ output/analysis_results.json.
    """
    print("Starting final report generation...")

    try:
        if analysis_results is None:
            analysis_results = _load_analysis_results()

        row_counts = _load_row_counts()

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        styles = _build_styles()
        doc = SimpleDocTemplate(
            str(FINAL_REPORT_PDF),
            pagesize=A4,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            title="BeautifulSoup Documentation Analytics - Final Report",
        )

        story = []
        story += _section_cover(styles, row_counts)
        story += _section_dataset_overview(styles, row_counts)
        story += _section_scraping_method(styles)
        story += _section_extracted_data_summary(styles, analysis_results)
        story.append(PageBreak())
        story += _section_analysis_results(styles, analysis_results)
        story.append(PageBreak())
        story += _section_charts(styles)
        story.append(PageBreak())
        story += _section_key_findings(styles, analysis_results, row_counts)
        story += _section_limitations(styles)
        story += _section_conclusion(styles, analysis_results, row_counts)

        doc.build(
            story,
            onFirstPage=_draw_page_number,
            onLaterPages=_draw_page_number,
        )

        print(f"Successfully exported {FINAL_REPORT_PDF.name}")
        return str(FINAL_REPORT_PDF)

    except Exception as e:
        print(f"Error during report generation: {e}")
        return None


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="BeautifulSoup Documentation Report Generator")
    arg_parser.parse_args()

    output_path = run_report_generator()
    if output_path is None:
        exit(1)
