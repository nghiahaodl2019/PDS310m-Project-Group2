"""
Feature 6: Documentation Analytics
Trả lời tối thiểu 8 câu hỏi bắt buộc + 2 câu hỏi bổ sung bằng Pandas và NumPy.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Giải quyết triệt để vấn đề đường dẫn (giống collector.py, parser.py, extractor.py, visualizer.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"

SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"

ANALYSIS_JSON = OUTPUT_DIR / "analysis_results.json"
SUMMARY_XLSX = OUTPUT_DIR / "summary_tables.xlsx"

# Stopword tối giản cho tiếng Anh (đủ dùng để lọc các từ nối phổ biến trong tài liệu kỹ thuật)
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "it", "you", "this",
    "that", "for", "on", "with", "as", "are", "be", "if", "your", "can", "will",
    "not", "by", "we", "at", "from", "which", "its", "has", "have", "was", "were",
    "but", "so", "all", "one", "when", "would", "there", "their", "what", "each",
    "into", "than", "then", "them", "these", "those", "also", "here", "how", "do",
    "does", "done", "just", "like", "may", "more", "no", "our", "out", "over",
    "such", "up", "use", "used", "using", "want", "way",
}

# Curated vocabulary used to keep Q5 focused on technical concepts instead of
# common prose and URL fragments such as "example" or "com".
TECHNICAL_KEYWORDS = {
    "attribute", "attributes", "beautifulsoup", "boolean", "bytes", "class",
    "css", "decode", "document", "element", "encoding", "find", "findall",
    "formatter", "html", "html5lib", "href", "id", "keyword", "link", "lxml",
    "markup", "method", "parser", "python", "request", "requests", "select",
    "selector", "soup", "string", "tag", "text", "tree", "unicode", "url",
    "xml",
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _load_from_csv() -> Dict[str, pd.DataFrame]:
    """Đọc lại 3 file CSV đã xử lý (dùng khi chạy analyzer.py độc lập)."""
    sections_df = pd.read_csv(SECTIONS_CSV, encoding="utf-8-sig")
    links_df = pd.read_csv(LINKS_CSV, encoding="utf-8-sig")
    code_examples_df = pd.read_csv(CODE_EXAMPLES_CSV, encoding="utf-8-sig")
    return {
        "sections": sections_df,
        "links": links_df,
        "code_examples": code_examples_df,
    }


def _tokenize(text: str) -> List[str]:
    """Tokenize text and retain terms from the documented technical vocabulary."""
    text = re.sub(r"https?://\S+|www\.\S+", " ", text.lower())
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return [
        word
        for word in words
        if len(word) >= 3
        and word not in STOPWORDS
        and word in TECHNICAL_KEYWORDS
    ]


# --------------------------------------------------------------------------
# 8 câu hỏi bắt buộc
# --------------------------------------------------------------------------

def q1_total_sections(sections_df: pd.DataFrame) -> int:
    """1. How many sections are in the documentation?"""
    return int(len(sections_df))


def q2_highest_word_count_section(sections_df: pd.DataFrame) -> Dict:
    """2. Which section has the highest word count?"""
    row = sections_df.loc[sections_df["word_count"].idxmax()]
    return {"section_title": row["section_title"], "word_count": int(row["word_count"])}


def q3_most_code_examples_section(sections_df: pd.DataFrame) -> Dict:
    """3. Which section contains the most code examples?"""
    row = sections_df.loc[sections_df["code_block_count"].idxmax()]
    return {"section_title": row["section_title"], "code_block_count": int(row["code_block_count"])}


def q4_most_links_section(sections_df: pd.DataFrame) -> Dict:
    """4. Which section contains the most links?"""
    row = sections_df.loc[sections_df["link_count"].idxmax()]
    return {"section_title": row["section_title"], "link_count": int(row["link_count"])}


def q5_top10_keywords(sections_df: pd.DataFrame, top_n: int = 10) -> List[Dict]:
    """5. What are the top 10 most frequent technical keywords?"""
    all_words: List[str] = []
    for text in sections_df["section_text"].dropna():
        all_words.extend(_tokenize(text))

    words_array = np.array(all_words)
    unique_words, counts = np.unique(words_array, return_counts=True)

    order = np.argsort(counts)[::-1][:top_n]
    top_words = unique_words[order]
    top_counts = counts[order]

    return [{"keyword": w, "frequency": int(c)} for w, c in zip(top_words, top_counts)]


def q6_internal_external_links(links_df: pd.DataFrame) -> Dict:
    """6. How many internal and external links exist?"""
    counts = links_df["link_type"].value_counts()
    return {
        "internal_anchor": int(counts.get("internal_anchor", 0)),
        "external_link": int(counts.get("external_link", 0)),
    }


def q7_find_all_usage(code_examples_df: pd.DataFrame) -> int:
    """7. How many code examples use find_all()?"""
    return int(code_examples_df["contains_find_all"].sum())


def q8_get_text_usage(code_examples_df: pd.DataFrame) -> int:
    """8. How many code examples use get_text()?"""
    return int(code_examples_df["contains_get_text"].sum())


# --------------------------------------------------------------------------
# 2 câu hỏi bổ sung
# --------------------------------------------------------------------------

def q9_word_count_statistics(sections_df: pd.DataFrame) -> Dict:
    """9 (bổ sung). Thống kê word_count trên toàn bộ section (mean, median, std) bằng NumPy."""
    values = sections_df["word_count"].to_numpy()
    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "min": int(np.min(values)),
        "max": int(np.max(values)),
    }


def q10_bs4_method_usage_ratio(code_examples_df: pd.DataFrame) -> Dict:
    """10 (bổ sung). Bao nhiêu % code examples có dùng ít nhất 1 trong 3 method
    tìm kiếm chính của BeautifulSoup (find_all / find / select)?"""
    total = len(code_examples_df)
    uses_any = (
            code_examples_df["contains_find_all"]
            | code_examples_df["contains_find"]
            | code_examples_df["contains_select"]
    ).sum()
    percentage = round(float(uses_any) / total * 100, 2) if total else 0.0
    return {
        "total_code_examples": int(total),
        "examples_using_search_methods": int(uses_any),
        "percentage": percentage,
    }


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def run_all_analytics(data: Optional[Dict[str, pd.DataFrame]] = None) -> Optional[Dict]:
    """
    Chạy toàn bộ 8 câu hỏi bắt buộc + 2 câu bổ sung, lưu kết quả ra
    output/analysis_results.json và output/summary_tables.xlsx.

    data: dict trả về từ run_all_extractions() (Feature 3-5), gồm
          "sections", "links", "code_examples". Nếu None, tự đọc lại từ CSV.
    """
    print("Starting analytics...")

    try:
        if data is None:
            data = _load_from_csv()

        sections_df = data["sections"]
        links_df = data["links"]
        code_examples_df = data["code_examples"]

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        results = {
            "q1_total_sections": q1_total_sections(sections_df),
            "q2_highest_word_count_section": q2_highest_word_count_section(sections_df),
            "q3_most_code_examples_section": q3_most_code_examples_section(sections_df),
            "q4_most_links_section": q4_most_links_section(sections_df),
            "q5_top10_keywords": q5_top10_keywords(sections_df),
            "q6_internal_external_links": q6_internal_external_links(links_df),
            "q7_find_all_usage": q7_find_all_usage(code_examples_df),
            "q8_get_text_usage": q8_get_text_usage(code_examples_df),
            "q9_word_count_statistics": q9_word_count_statistics(sections_df),
            "q10_bs4_method_usage_ratio": q10_bs4_method_usage_ratio(code_examples_df),
        }

        # Lưu JSON đầy đủ (để report_generator.py ở Feature 8 dùng lại)
        with open(ANALYSIS_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Successfully exported {ANALYSIS_JSON.name}")

        # Lưu bảng tổng hợp dạng Excel (dễ đọc, dùng để tham chiếu trong report)
        _save_summary_xlsx(results)
        print(f"Successfully exported {SUMMARY_XLSX.name}")

        return results

    except Exception as e:
        print(f"Error during analytics: {e}")
        return None


def _save_summary_xlsx(results: Dict) -> None:
    """Ghi kết quả phân tích ra output/summary_tables.xlsx (nhiều sheet)."""
    qa_rows = [
        ("Q1", "How many sections are in the documentation?",
         results["q1_total_sections"]),
        ("Q2", "Which section has the highest word count?",
         f'{results["q2_highest_word_count_section"]["section_title"]} '
         f'({results["q2_highest_word_count_section"]["word_count"]} words)'),
        ("Q3", "Which section contains the most code examples?",
         f'{results["q3_most_code_examples_section"]["section_title"]} '
         f'({results["q3_most_code_examples_section"]["code_block_count"]} examples)'),
        ("Q4", "Which section contains the most links?",
         f'{results["q4_most_links_section"]["section_title"]} '
         f'({results["q4_most_links_section"]["link_count"]} links)'),
        ("Q5", "What are the top 10 most frequent technical keywords?",
         ", ".join(k["keyword"] for k in results["q5_top10_keywords"])),
        ("Q6", "How many internal and external links exist?",
         f'internal_anchor={results["q6_internal_external_links"]["internal_anchor"]}, '
         f'external_link={results["q6_internal_external_links"]["external_link"]}'),
        ("Q7", "How many code examples use find_all()?",
         results["q7_find_all_usage"]),
        ("Q8", "How many code examples use get_text()?",
         results["q8_get_text_usage"]),
        ("Q9 (extra)", "Word count statistics across sections (mean/median/std)",
         f'mean={results["q9_word_count_statistics"]["mean"]:.1f}, '
         f'median={results["q9_word_count_statistics"]["median"]:.1f}, '
         f'std={results["q9_word_count_statistics"]["std"]:.1f}'),
        ("Q10 (extra)", "% code examples using find_all/find/select",
         f'{results["q10_bs4_method_usage_ratio"]["percentage"]}%'),
    ]
    qa_df = pd.DataFrame(qa_rows, columns=["question_id", "question", "answer"])
    keywords_df = pd.DataFrame(results["q5_top10_keywords"])

    with pd.ExcelWriter(SUMMARY_XLSX, engine="openpyxl") as writer:
        qa_df.to_excel(writer, sheet_name="Answers", index=False)
        keywords_df.to_excel(writer, sheet_name="Top_Keywords", index=False)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="BeautifulSoup Documentation Analyzer")
    arg_parser.parse_args()

    output = run_all_analytics()
    if output is None:
        exit(1)
