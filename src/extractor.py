"""
Features 3, 4, 5: Section / Link / Code Example Extractor
"""

import argparse
import copy
import re
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse

import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Comment

# Import đúng hàm từ module parser.py
from parser import parse_webpage, DEFAULT_INPUT_PATH

# Giải quyết triệt để vấn đề đường dẫn (giống collector.py và parser.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SECTIONS_CSV = PROCESSED_DIR / "sections.csv"
LINKS_CSV = PROCESSED_DIR / "links.csv"
CODE_EXAMPLES_CSV = PROCESSED_DIR / "code_examples.csv"

HEADING_TAGS = ["h1", "h2", "h3"]
DOC_DOMAIN = "crummy.com"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _heading_title(heading) -> str:
    """Lấy text sạch của 1 heading, loại bỏ các thẻ <a class="headerlink">."""
    heading_copy = copy.copy(heading)
    for anchor in heading_copy.find_all("a", class_="headerlink"):
        anchor.decompose()
    title = heading_copy.get_text(strip=True)
    return title.rstrip("¶").strip()


def _clean_text(elem) -> str:
    """Lấy text của 1 NavigableString, bỏ qua script/style/comment."""
    if isinstance(elem, Comment):
        return ""
    if not isinstance(elem, NavigableString):
        return ""
    parent_name = elem.parent.name if elem.parent else ""
    if parent_name in ("script", "style"):
        return ""
    return str(elem)


def _classify_link(href: str) -> str:
    """Phân loại 1 href theo 5 nhóm được yêu cầu."""
    if href is None or href.strip() == "" or href.strip().lower() in ("#", "javascript:void(0)"):
        return "empty_or_invalid"

    href = href.strip()

    if href.startswith("#"):
        return "internal_anchor"

    lower_href = href.lower().split("?")[0].split("#")[0]
    if lower_href.endswith(IMAGE_EXTENSIONS):
        return "image_link"

    parsed = urlparse(href)
    if parsed.scheme in ("http", "https"):
        if DOC_DOMAIN in parsed.netloc:
            return "documentation_link"
        return "external_link"

    if parsed.scheme in ("mailto", "javascript"):
        return "empty_or_invalid"

    return "documentation_link"


def _nearest_section_title(tag, headings) -> str:
    """Tìm heading gần nhất phía trước `tag` trong document order."""
    preceding = tag.find_previous(HEADING_TAGS)
    if preceding is not None:
        return _heading_title(preceding)
    return ""


# --------------------------------------------------------------------------
# Feature 3, 4, 5 Extractors
# --------------------------------------------------------------------------

def extract_sections(soup: BeautifulSoup) -> pd.DataFrame:
    """Trích xuất tất cả section (dựa trên heading h1/h2/h3)."""
    headings = soup.find_all(HEADING_TAGS)
    rows = []

    for idx, heading in enumerate(headings):
        level = int(heading.name[1])
        title = _heading_title(heading)
        next_heading = headings[idx + 1] if idx + 1 < len(headings) else None

        text_parts = []
        code_block_count = 0
        link_count = 0

        for elem in heading.next_elements:
            if next_heading is not None and elem is next_heading:
                break
            if getattr(elem, "name", None) == "pre":
                code_block_count += 1
            elif getattr(elem, "name", None) == "a" and elem.get("href"):
                link_count += 1
            else:
                text_parts.append(_clean_text(elem))

        section_text = " ".join(t.strip() for t in text_parts if t.strip())
        section_text = re.sub(r"\s+", " ", section_text).strip()
        word_count = len(section_text.split()) if section_text else 0

        rows.append({
            "section_id": idx + 1,
            "section_level": level,
            "section_title": title,
            "section_text": section_text,
            "word_count": word_count,
            "code_block_count": code_block_count,
            "link_count": link_count,
        })

    return pd.DataFrame(rows)


def extract_links(soup: BeautifulSoup) -> pd.DataFrame:
    """Trích xuất mọi hyperlink trong tài liệu."""
    headings = soup.find_all(HEADING_TAGS)
    rows = []

    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")
        link_text = a_tag.get_text(strip=True)
        link_type = _classify_link(href)
        section_title = _nearest_section_title(a_tag, headings)

        rows.append({
            "link_text": link_text,
            "href": href if href is not None else "",
            "link_type": link_type,
            "section_title": section_title,
        })

    return pd.DataFrame(rows)


def extract_code_examples(soup: BeautifulSoup) -> pd.DataFrame:
    """Trích xuất mọi đoạn code ví dụ Python (nằm trong thẻ <pre>)."""
    headings = soup.find_all(HEADING_TAGS)
    rows = []

    pre_tags = soup.find_all("pre")
    for idx, pre in enumerate(pre_tags):
        code_text = pre.get_text()
        code_text_clean = code_text.strip("\n")
        line_count = len(code_text_clean.splitlines()) if code_text_clean else 0
        section_title = _nearest_section_title(pre, headings)

        rows.append({
            "example_id": idx + 1,
            "section_title": section_title,
            "code_text": code_text_clean,
            "line_count": line_count,
            "contains_find_all": ("find_all(" in code_text) or ("findAll(" in code_text),
            "contains_find": ".find(" in code_text or code_text.strip().startswith("find("),
            "contains_select": ("select(" in code_text) or ("select_one(" in code_text),
            "contains_get_text": "get_text(" in code_text,
            "contains_requests": "requests." in code_text or "import requests" in code_text,
        })

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def run_all_extractions(input_path: str = DEFAULT_INPUT_PATH) -> Optional[Dict[str, pd.DataFrame]]:
    """Chạy cả 3 extractor và lưu ra CSV."""
    print(f"Starting extractions from parsed HTML: {input_path}")

    try:
        # Sử dụng parse_webpage từ file parser.py để lấy soup
        soup = parse_webpage(input_path)

        # Đảm bảo thư mục đích tồn tại sử dụng pathlib
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

        sections_df = extract_sections(soup)
        links_df = extract_links(soup)
        code_examples_df = extract_code_examples(soup)

        # Lưu CSV
        sections_df.to_csv(SECTIONS_CSV, index=False, encoding="utf-8-sig")
        links_df.to_csv(LINKS_CSV, index=False, encoding="utf-8-sig")
        code_examples_df.to_csv(CODE_EXAMPLES_CSV, index=False, encoding="utf-8-sig")

        print(f"Successfully exported {SECTIONS_CSV.name}: {len(sections_df)} rows")
        print(f"Successfully exported {LINKS_CSV.name}: {len(links_df)} rows")
        print(f"Successfully exported {CODE_EXAMPLES_CSV.name}: {len(code_examples_df)} rows")

        return {
            "sections": sections_df,
            "links": links_df,
            "code_examples": code_examples_df,
        }
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BeautifulSoup Document Extractor")
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_PATH,
        help="Path to the raw HTML file to extract data from"
    )

    args = parser.parse_args()
    results = run_all_extractions(input_path=args.input)
    if results is None:
        exit(1)