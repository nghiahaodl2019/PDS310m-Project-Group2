"""
Feature 7: Data Visualization
"""

import argparse
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import matplotlib.pyplot as plt

# Giải quyết triệt để vấn đề đường dẫn (giống collector.py, parser.py, extractor.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHARTS_DIR = PROJECT_ROOT / "output" / "charts"

SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"

CODE_EXAMPLES_TOP_N = 15  # số section hiển thị trên bar chart "code examples by section"


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _load_from_csv() -> Dict[str, pd.DataFrame]:
    """Đọc lại 3 file CSV đã xử lý (dùng khi chạy visualizer.py độc lập)."""
    sections_df = pd.read_csv(SECTIONS_CSV, encoding="utf-8-sig")
    links_df = pd.read_csv(LINKS_CSV, encoding="utf-8-sig")
    code_examples_df = pd.read_csv(CODE_EXAMPLES_CSV, encoding="utf-8-sig")
    return {
        "sections": sections_df,
        "links": links_df,
        "code_examples": code_examples_df,
    }


# --------------------------------------------------------------------------
# Feature 7 Charts
# --------------------------------------------------------------------------

def chart_top10_sections_by_wordcount(sections_df: pd.DataFrame) -> Path:
    """Bar chart: Top 10 sections theo word_count."""
    top10 = sections_df.sort_values("word_count", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(top10["section_title"], top10["word_count"], color="#4C72B0")
    plt.xlabel("Word Count")
    plt.ylabel("Section")
    plt.title("Top 10 Sections by Word Count")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    out_path = CHARTS_DIR / "word_count_by_section.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


def chart_code_examples_by_section(code_examples_df: pd.DataFrame, top_n: int = CODE_EXAMPLES_TOP_N) -> Path:
    """Bar chart: Số lượng code examples theo section."""
    counts = (
        code_examples_df.groupby("section_title")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(counts.index, counts.values, color="#DD8452")
    plt.xlabel("Number of Code Examples")
    plt.ylabel("Section")
    plt.title(f"Top {top_n} Sections by Number of Code Examples")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    out_path = CHARTS_DIR / "code_examples_by_section.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


def chart_link_type_distribution(links_df: pd.DataFrame) -> Path:
    """Pie chart: Phân bố link_type."""
    type_counts = links_df["link_type"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = plt.cm.Pastel1.colors

    wedges, _, _ = ax.pie(
        type_counts.values,
        labels=None,  # Không đặt label trực tiếp để tránh chồng chữ
        autopct=lambda pct: f"{pct:.1f}%" if pct >= 2 else "",
        startangle=90,
        colors=colors[:len(type_counts)],
        pctdistance=0.7,
    )

    ax.set_title("Link Type Distribution", pad=18)
    ax.legend(
        wedges,
        [f"{link_type} ({count})" for link_type, count in type_counts.items()],
        title="Link type",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    ax.axis("equal")

    out_path = CHARTS_DIR / "link_type_distribution.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_code_linecount_histogram(code_examples_df: pd.DataFrame, bins: int = 20) -> Path:
    """Histogram: Phân bố line_count của code examples."""
    plt.figure(figsize=(10, 6))
    plt.hist(code_examples_df["line_count"], bins=bins, color="#55A868", edgecolor="black")
    plt.xlabel("Line Count per Code Example")
    plt.ylabel("Frequency")
    plt.title("Distribution of Code Example Line Counts")
    plt.tight_layout()

    out_path = CHARTS_DIR / "code_linecount_hist.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def run_all_visualizations(data: Optional[Dict[str, pd.DataFrame]] = None) -> Optional[Dict[str, str]]:
    """
    Chạy cả 4 chart bắt buộc và lưu ra output/charts/.

    data: dict trả về từ run_all_extractions() (Feature 3-5), gồm
          "sections", "links", "code_examples". Nếu None, tự đọc lại từ CSV.
    """
    print("Starting visualizations...")

    try:
        if data is None:
            data = _load_from_csv()

        sections_df = data["sections"]
        links_df = data["links"]
        code_examples_df = data["code_examples"]

        CHARTS_DIR.mkdir(parents=True, exist_ok=True)

        chart_paths = {
            "word_count_by_section": chart_top10_sections_by_wordcount(sections_df),
            "code_examples_by_section": chart_code_examples_by_section(code_examples_df),
            "link_type_distribution": chart_link_type_distribution(links_df),
            "code_linecount_hist": chart_code_linecount_histogram(code_examples_df),
        }

        for name, path in chart_paths.items():
            print(f"Successfully exported {path.name}")

        return {name: str(path) for name, path in chart_paths.items()}

    except Exception as e:
        print(f"Error during visualization: {e}")
        return None


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="BeautifulSoup Documentation Visualizer")
    arg_parser.parse_args()

    results = run_all_visualizations()
    if results is None:
        exit(1)