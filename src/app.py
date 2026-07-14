"""
Advanced Requirement - Option B: Local Streamlit application.

Run with:
    streamlit run src/app.py
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from collector import collect_webpage
from parser import run_parser
from extractor import run_all_extractions
from analyzer import run_all_analytics
from visualizer import run_all_visualizations
from report_generator import run_report_generator


PROJECT_ROOT = _SRC_DIR.parent
SECTIONS_CSV = PROJECT_ROOT / "data" / "processed" / "sections.csv"
LINKS_CSV = PROJECT_ROOT / "data" / "processed" / "links.csv"
CODE_CSV = PROJECT_ROOT / "data" / "processed" / "code_examples.csv"
SUMMARY_XLSX = PROJECT_ROOT / "output" / "summary_tables.xlsx"
CHARTS_DIR = PROJECT_ROOT / "output" / "charts"
FINAL_REPORT_PDF = PROJECT_ROOT / "output" / "final_report.pdf"

CHART_LABELS = {
    "word_count_by_section.png": "Top 10 Sections by Word Count",
    "code_examples_by_section.png": "Code Examples by Section",
    "link_type_distribution.png": "Link Type Distribution",
    "code_linecount_hist.png": "Code Example Line Count Distribution",
}


st.set_page_config(
    page_title="BeautifulSoup Analytics",
    page_icon="BS",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

    :root {
        --ink: #14213d;
        --muted: #667085;
        --primary: #5b5fef;
        --primary-dark: #4246d9;
        --cyan: #0ea5b7;
        --surface: rgba(255, 255, 255, 0.92);
        --border: #e5e9f2;
    }

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 83% 2%, rgba(91, 95, 239, 0.10), transparent 24rem),
            radial-gradient(circle at 28% 88%, rgba(14, 165, 183, 0.07), transparent 26rem),
            #f7f9fc;
    }

    [data-testid="stHeader"] { background: transparent; }

    .main .block-container {
        max-width: 1440px;
        padding: 2rem 2.4rem 4rem;
    }

    h1, h2, h3, h4 {
        font-family: "Manrope", sans-serif !important;
        letter-spacing: -0.025em;
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 15% 15%, rgba(123, 128, 255, 0.28), transparent 13rem),
            linear-gradient(165deg, #151a35 0%, #20264b 55%, #172038 100%);
        border-right: 0;
    }

    [data-testid="stSidebar"] * { color: #f8fafc; }
    [data-testid="stSidebar"] .stCaption { color: #b9c2d7 !important; }
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        background: rgba(255,255,255,0.04);
    }

    [data-testid="stSidebar"] .stButton > button {
        border-radius: 11px;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.07);
        color: white;
        font-weight: 600;
        transition: transform 160ms ease, background 160ms ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.13);
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #777bf8, #5b5fef);
        border: none;
        box-shadow: 0 8px 22px rgba(91,95,239,0.32);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0.25rem 0 1.6rem;
    }

    .brand-mark {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 13px;
        background: linear-gradient(135deg, #7b80ff, #35c3cc);
        font-family: "Manrope", sans-serif;
        font-size: 0.82rem;
        font-weight: 800;
        color: white;
        box-shadow: 0 10px 26px rgba(53,195,204,0.2);
    }

    .brand-title { font-weight: 700; font-size: 1rem; color: white; }
    .brand-subtitle { color: #aeb8cf; font-size: 0.74rem; margin-top: 2px; }

    .sidebar-status {
        padding: 13px 14px;
        margin: 0.8rem 0 1.2rem;
        border: 1px solid rgba(255,255,255,0.11);
        border-radius: 13px;
        background: rgba(255,255,255,0.055);
    }

    .sidebar-status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.79rem;
        margin-bottom: 9px;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 7px;
        border-radius: 999px;
        background: #45d4a8;
        box-shadow: 0 0 0 4px rgba(69,212,168,0.12);
    }

    .progress-track {
        height: 5px;
        border-radius: 99px;
        background: rgba(255,255,255,0.12);
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #6d72f3, #38c7c5);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.3rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(91,95,239,0.12);
        border-radius: 24px;
        background: linear-gradient(130deg, rgba(255,255,255,0.98), rgba(246,247,255,0.94));
        box-shadow: 0 18px 55px rgba(38, 48, 93, 0.08);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 290px;
        height: 290px;
        right: -70px;
        top: -130px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(91,95,239,0.2), rgba(14,165,183,0.15));
    }

    .eyebrow {
        color: var(--primary);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .hero h1 {
        max-width: 820px;
        margin: 0;
        font-size: clamp(2rem, 3.1vw, 3.1rem);
        line-height: 1.08;
    }

    .hero p {
        max-width: 720px;
        margin: 1rem 0 1.2rem;
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.7;
    }

    .hero-pill {
        display: inline-flex;
        align-items: center;
        margin-right: 8px;
        padding: 6px 10px;
        border: 1px solid #e3e6f6;
        border-radius: 999px;
        background: white;
        color: #4b5270;
        font-size: 0.73rem;
        font-weight: 600;
    }

    .metric-card {
        min-height: 130px;
        padding: 1.25rem 1.35rem;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: var(--surface);
        box-shadow: 0 10px 28px rgba(39, 47, 84, 0.055);
    }

    .metric-accent {
        width: 35px;
        height: 4px;
        margin-bottom: 1rem;
        border-radius: 99px;
    }

    .metric-label { color: var(--muted); font-size: 0.78rem; font-weight: 600; }
    .metric-value { margin: 3px 0; font-family: "Manrope", sans-serif; font-size: 2rem; font-weight: 800; }
    .metric-detail { color: #8a93a8; font-size: 0.72rem; }

    .section-card {
        padding: 1.35rem 1.5rem;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: rgba(255,255,255,0.86);
        box-shadow: 0 10px 28px rgba(39,47,84,0.045);
    }

    .section-kicker { color: var(--primary); font-size: 0.7rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
    .section-title { margin: 5px 0 7px; font-family: "Manrope", sans-serif; font-size: 1.12rem; font-weight: 700; }
    .section-copy { color: var(--muted); font-size: 0.84rem; line-height: 1.55; }

    .workflow {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 8px;
        margin: 1rem 0 0.25rem;
    }

    .workflow-step {
        padding: 11px 8px;
        border: 1px solid #e4e7f1;
        border-radius: 11px;
        background: #fafbfe;
        color: #525b70;
        font-size: 0.72rem;
        font-weight: 600;
        text-align: center;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        padding: 5px;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: rgba(255,255,255,0.8);
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        padding: 0 15px;
        border-radius: 10px;
        color: #697188;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: #eef0ff !important;
        color: var(--primary) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    [data-testid="stDataFrame"] {
        overflow: hidden;
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(39,47,84,0.04);
    }

    .stDownloadButton > button, .main .stButton > button {
        border-radius: 11px;
        border: 1px solid #dfe3ee;
        font-weight: 600;
    }

    .stDownloadButton > button:hover, .main .stButton > button:hover {
        border-color: var(--primary);
        color: var(--primary);
    }

    [data-testid="stFileUploaderDropzone"], [data-testid="stAlert"] { border-radius: 14px; }
    hr { border-color: #e8ebf3; }

    @media (max-width: 900px) {
        .main .block-container { padding: 1.2rem 1rem 3rem; }
        .hero { padding: 1.6rem; }
        .workflow { grid-template-columns: repeat(2, 1fr); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "extraction_results" not in st.session_state:
    st.session_state.extraction_results = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None


@st.cache_data(show_spinner=False)
def load_datasets():
    if not all(path.exists() for path in (SECTIONS_CSV, LINKS_CSV, CODE_CSV)):
        return None
    return {
        "sections": pd.read_csv(SECTIONS_CSV, encoding="utf-8-sig"),
        "links": pd.read_csv(LINKS_CSV, encoding="utf-8-sig"),
        "code": pd.read_csv(CODE_CSV, encoding="utf-8-sig"),
    }


def refresh_data_cache():
    load_datasets.clear()


def artifact_progress():
    artifacts = [
        PROJECT_ROOT / "data" / "raw" / "beautifulsoup_doc.html",
        SECTIONS_CSV,
        LINKS_CSV,
        CODE_CSV,
        SUMMARY_XLSX,
        CHARTS_DIR / "word_count_by_section.png",
        CHARTS_DIR / "link_type_distribution.png",
        FINAL_REPORT_PDF,
    ]
    completed = sum(path.exists() for path in artifacts)
    return completed, len(artifacts)


def step_collect():
    with st.spinner("Downloading the documentation page..."):
        ok = collect_webpage()
    st.toast("Web page collected." if ok else "Collection failed.")
    return ok


def step_parse():
    with st.spinner("Parsing HTML with BeautifulSoup..."):
        soup = run_parser()
    st.toast("HTML parsed." if soup is not None else "Parsing failed.")
    return soup


def step_extract():
    with st.spinner("Extracting sections, links, and code examples..."):
        results = run_all_extractions()
    if results is not None:
        st.session_state.extraction_results = results
        refresh_data_cache()
        st.toast("Structured datasets created.")
    else:
        st.error("Extraction failed. Collect the page first.")
    return results


def step_analyze():
    with st.spinner("Running Pandas and NumPy analytics..."):
        results = run_all_analytics(st.session_state.extraction_results)
    if results is not None:
        st.session_state.analysis_results = results
        st.toast("Analytics completed.")
    else:
        st.error("Analytics failed. Extract the datasets first.")
    return results


def step_visualize():
    with st.spinner("Rendering four analytical charts..."):
        results = run_all_visualizations(st.session_state.extraction_results)
    st.toast("Charts generated." if results is not None else "Chart generation failed.")
    return results


def step_report():
    with st.spinner("Compiling the final PDF report..."):
        path = run_report_generator(st.session_state.analysis_results)
    st.toast("Final report created." if path is not None else "Report generation failed.")
    return path


def run_full_pipeline():
    with st.status("Running the complete analytics pipeline", expanded=True) as status:
        stages = [
            ("01  Collecting source HTML", collect_webpage),
            ("02  Parsing document structure", run_parser),
            ("03  Extracting structured datasets", run_all_extractions),
        ]
        results = {}
        for label, action in stages:
            st.write(label)
            result = action()
            if result is False or result is None:
                status.update(label=f"Pipeline stopped at {label}", state="error")
                return
            results[label] = result

        extraction = results["03  Extracting structured datasets"]
        st.session_state.extraction_results = extraction

        st.write("04  Running ten analytical questions")
        analysis = run_all_analytics(extraction)
        if analysis is None:
            status.update(label="Pipeline stopped during analytics", state="error")
            return
        st.session_state.analysis_results = analysis

        st.write("05  Generating visualizations")
        if run_all_visualizations(extraction) is None:
            status.update(label="Pipeline stopped during visualization", state="error")
            return

        st.write("06  Building the final report")
        if run_report_generator(analysis) is None:
            status.update(label="Pipeline stopped during report generation", state="error")
            return

        refresh_data_cache()
        st.session_state.last_run = datetime.now().strftime("%d %b %Y, %H:%M")
        status.update(label="Pipeline completed successfully", state="complete", expanded=False)
    st.rerun()


def metric_card(label, value, detail, color):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-accent" style="background:{color}"></div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(kicker, title, copy):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            <div class="section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dataset_toolbar(title, description, frame, filename):
    title_col, download_col = st.columns([0.78, 0.22], vertical_alignment="center")
    with title_col:
        st.subheader(title)
        st.caption(description)
    with download_col:
        st.download_button(
            "Export CSV",
            frame.to_csv(index=False).encode("utf-8-sig"),
            filename,
            "text/csv",
            use_container_width=True,
        )


completed, total = artifact_progress()
progress_percent = round(completed / total * 100)

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">BS4</div>
            <div>
                <div class="brand-title">Doc Intelligence</div>
                <div class="brand-subtitle">BeautifulSoup Analytics</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("PIPELINE CONTROL")
    st.markdown(
        f"""
        <div class="sidebar-status">
            <div class="sidebar-status-row">
                <span><span class="status-dot"></span>{'Ready' if completed == total else 'Setup required'}</span>
                <span>{completed}/{total}</span>
            </div>
            <div class="progress-track"><div class="progress-fill" style="width:{progress_percent}%"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Run full pipeline", type="primary", use_container_width=True):
        run_full_pipeline()

    with st.expander("Run step by step"):
        if st.button("01  Collect web page", use_container_width=True):
            step_collect()
        if st.button("02  Parse HTML", use_container_width=True):
            step_parse()
        if st.button("03  Extract datasets", use_container_width=True):
            step_extract()
        if st.button("04  Run analytics", use_container_width=True):
            step_analyze()
        if st.button("05  Generate charts", use_container_width=True):
            step_visualize()
        if st.button("06  Build PDF report", use_container_width=True):
            step_report()

    st.divider()
    st.caption("SOURCE")
    st.markdown("[Beautiful Soup 4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)")
    if FINAL_REPORT_PDF.exists():
        st.caption(f"Report updated {datetime.fromtimestamp(FINAL_REPORT_PDF.stat().st_mtime).strftime('%d %b %Y, %H:%M')}")


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Documentation intelligence platform</div>
        <h1>Turn technical documentation into structured insight.</h1>
        <p>Collect, parse, analyze, and visualize the official Beautiful Soup documentation through one reproducible Python workflow.</p>
        <span class="hero-pill">Python</span>
        <span class="hero-pill">BeautifulSoup</span>
        <span class="hero-pill">Pandas + NumPy</span>
        <span class="hero-pill">Automated PDF report</span>
    </div>
    """,
    unsafe_allow_html=True,
)

header_left, header_right = st.columns([0.76, 0.24], vertical_alignment="center")
with header_left:
    st.subheader("Analytics workspace")
    st.caption("Explore extracted datasets, analytical answers, and final visualizations.")
with header_right:
    if FINAL_REPORT_PDF.exists():
        with open(FINAL_REPORT_PDF, "rb") as report_file:
            st.download_button(
                "Download final report",
                report_file,
                "final_report.pdf",
                "application/pdf",
                use_container_width=True,
            )


datasets = load_datasets()
tab_overview, tab_sections, tab_links, tab_code, tab_analytics, tab_charts = st.tabs(
    ["Overview", "Sections", "Links", "Code", "Analytics", "Visualizations"]
)


with tab_overview:
    st.write("")
    if datasets is None:
        st.info("No processed data found. Run the full pipeline from the sidebar to begin.")
    else:
        sections_df = datasets["sections"]
        links_df = datasets["links"]
        code_df = datasets["code"]

        metric_columns = st.columns(4)
        with metric_columns[0]:
            metric_card("DOCUMENT SECTIONS", f"{len(sections_df):,}", "Structured headings extracted", "#5b5fef")
        with metric_columns[1]:
            metric_card("HYPERLINKS", f"{len(links_df):,}", "Classified into five link types", "#0ea5b7")
        with metric_columns[2]:
            metric_card("CODE EXAMPLES", f"{len(code_df):,}", "Python and BeautifulSoup snippets", "#e0844d")
        with metric_columns[3]:
            metric_card("PIPELINE STATUS", f"{progress_percent}%", f"{completed} of {total} artifacts ready", "#45b58a")

        st.write("")
        profile_left, profile_right = st.columns([0.58, 0.42])
        top_section = sections_df.loc[sections_df["word_count"].idxmax()]
        dominant_link = links_df["link_type"].value_counts().idxmax()
        dominant_count = int(links_df["link_type"].value_counts().max())

        with profile_left:
            section_card(
                "CONTENT PROFILE",
                f"{top_section['section_title']} leads with {int(top_section['word_count']):,} words",
                "The longest section is the most content-dense area of the documentation and a strong candidate for focused review.",
            )
            st.markdown(
                """
                <div class="workflow">
                    <div class="workflow-step">01 Collect</div>
                    <div class="workflow-step">02 Parse</div>
                    <div class="workflow-step">03 Extract</div>
                    <div class="workflow-step">04 Analyze</div>
                    <div class="workflow-step">05 Visualize</div>
                    <div class="workflow-step">06 Report</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with profile_right:
            section_card(
                "LINK LANDSCAPE",
                f"{dominant_count:,} {dominant_link.replace('_', ' ')} links",
                "Internal navigation dominates the documentation, showing a strongly connected single-page reference structure.",
            )

        st.write("")
        st.subheader("Dataset snapshot")
        preview = sections_df[["section_title", "section_level", "word_count", "code_block_count", "link_count"]].head(8)
        st.dataframe(preview, use_container_width=True, hide_index=True, height=320)


with tab_sections:
    if datasets is None:
        st.info("Sections data is not available yet.")
    else:
        sections_df = datasets["sections"]
        dataset_toolbar("Documentation sections", "Search and compare extracted section-level metrics.", sections_df, "sections.csv")
        filter_col, level_col = st.columns([0.72, 0.28])
        with filter_col:
            section_query = st.text_input("Search section title", placeholder="Try: parser, CSS, encoding...", key="section_search")
        with level_col:
            levels = sorted(sections_df["section_level"].unique().tolist())
            selected_levels = st.multiselect("Heading level", levels, default=levels)
        filtered_sections = sections_df[sections_df["section_level"].isin(selected_levels)]
        if section_query:
            filtered_sections = filtered_sections[
                filtered_sections["section_title"].str.contains(section_query, case=False, na=False)
            ]
        st.caption(f"Showing {len(filtered_sections):,} of {len(sections_df):,} sections")
        st.dataframe(filtered_sections, use_container_width=True, hide_index=True, height=560)


with tab_links:
    if datasets is None:
        st.info("Links data is not available yet.")
    else:
        links_df = datasets["links"]
        dataset_toolbar("Hyperlink inventory", "Filter every extracted URL by type and text.", links_df, "links.csv")
        search_col, type_col = st.columns([0.65, 0.35])
        with search_col:
            link_query = st.text_input("Search links", placeholder="Text, URL, or section...", key="link_search")
        with type_col:
            link_types = sorted(links_df["link_type"].unique().tolist())
            selected_types = st.multiselect("Link type", link_types, default=link_types)
        filtered_links = links_df[links_df["link_type"].isin(selected_types)]
        if link_query:
            mask = (
                filtered_links["link_text"].str.contains(link_query, case=False, na=False)
                | filtered_links["href"].str.contains(link_query, case=False, na=False)
                | filtered_links["section_title"].str.contains(link_query, case=False, na=False)
            )
            filtered_links = filtered_links[mask]
        st.caption(f"Showing {len(filtered_links):,} of {len(links_df):,} links")
        st.dataframe(filtered_links, use_container_width=True, hide_index=True, height=560)


with tab_code:
    if datasets is None:
        st.info("Code example data is not available yet.")
    else:
        code_df = datasets["code"]
        dataset_toolbar("Code example library", "Inspect examples and method-usage flags extracted from the documentation.", code_df, "code_examples.csv")
        method_filter = st.selectbox(
            "Filter by method",
            ["All examples", "find_all()", "find()", "select()", "get_text()", "requests"],
        )
        method_columns = {
            "find_all()": "contains_find_all",
            "find()": "contains_find",
            "select()": "contains_select",
            "get_text()": "contains_get_text",
            "requests": "contains_requests",
        }
        filtered_code = code_df if method_filter == "All examples" else code_df[code_df[method_columns[method_filter]]]
        st.caption(f"Showing {len(filtered_code):,} of {len(code_df):,} code examples")
        display_columns = [column for column in filtered_code.columns if column != "code_text"]
        st.dataframe(filtered_code[display_columns], use_container_width=True, hide_index=True, height=330)
        if not filtered_code.empty:
            example_options = filtered_code["example_id"].tolist()
            selected_example = st.selectbox("Preview example", example_options, format_func=lambda value: f"Example {value}")
            selected_row = filtered_code.loc[filtered_code["example_id"] == selected_example].iloc[0]
            st.caption(f"Section: {selected_row['section_title']} · {int(selected_row['line_count'])} lines")
            st.code(selected_row["code_text"], language="python")


with tab_analytics:
    if not SUMMARY_XLSX.exists():
        st.info("Analytics output is not available yet.")
    else:
        qa_df = pd.read_excel(SUMMARY_XLSX, sheet_name="Answers")
        keywords_df = pd.read_excel(SUMMARY_XLSX, sheet_name="Top_Keywords")
        analytics_header, excel_download = st.columns([0.76, 0.24], vertical_alignment="center")
        with analytics_header:
            st.subheader("Analytical findings")
            st.caption("Eight required questions and two team-proposed extensions.")
        with excel_download:
            with open(SUMMARY_XLSX, "rb") as summary_file:
                st.download_button(
                    "Export Excel summary",
                    summary_file,
                    "summary_tables.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
        answers_col, keyword_col = st.columns([0.62, 0.38])
        with answers_col:
            st.markdown("#### Question library")
            st.dataframe(qa_df, use_container_width=True, hide_index=True, height=445)
        with keyword_col:
            st.markdown("#### Technical vocabulary")
            st.bar_chart(keywords_df.set_index("keyword")["frequency"], height=400, color="#5b5fef")


with tab_charts:
    chart_files = [path for path in CHART_LABELS if (CHARTS_DIR / path).exists()]
    if not chart_files:
        st.info("Visualization files are not available yet.")
    else:
        st.subheader("Visualization gallery")
        st.caption("Four required charts generated by Matplotlib and embedded in the final report.")
        chart_columns = st.columns(2)
        for index, filename in enumerate(chart_files):
            chart_path = CHARTS_DIR / filename
            with chart_columns[index % 2]:
                with st.container(border=True):
                    st.markdown(f"#### {CHART_LABELS[filename]}")
                    st.image(str(chart_path), use_container_width=True)
