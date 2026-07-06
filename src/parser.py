import argparse
import os
from pathlib import Path
from typing import Dict, Optional

from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "beautifulsoup_doc.html"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "html_summary.csv"


def load_html(input_path: str = DEFAULT_INPUT_PATH) -> str:
    """
    Load raw HTML from disk.

    Args:
        input_path: Path to the downloaded HTML file.

    Returns:
        Raw HTML content as a string.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"HTML file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as file:
        return file.read()


def parse_html(html_content: str) -> BeautifulSoup:
    """
    Parse HTML content with BeautifulSoup.

    Args:
        html_content: Raw HTML content.

    Returns:
        BeautifulSoup object for downstream extraction.
    """
    return BeautifulSoup(html_content, "html.parser")


def summarize_document(soup: BeautifulSoup) -> Dict[str, int]:
    """
    Build a small structural summary of the parsed document.

    This gives Feature 2 a visible output and prepares the parsed tree for
    Feature 3 and later extractions.
    """
    return {
        "title": 1 if soup.title and soup.title.get_text(strip=True) else 0,
        "headings": len(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])),
        "paragraphs": len(soup.find_all("p")),
        "links": len(soup.find_all("a")),
        "code_blocks": len(soup.find_all(["code", "pre"])),
    }


def parse_webpage(input_path: str = DEFAULT_INPUT_PATH) -> BeautifulSoup:
    """
    Load and parse the downloaded HTML page.

    Args:
        input_path: Path to the raw HTML file.

    Returns:
        Parsed BeautifulSoup object.
    """
    html_content = load_html(input_path)
    soup = parse_html(html_content)
    return soup


def run_parser(input_path: str = DEFAULT_INPUT_PATH) -> Optional[BeautifulSoup]:
    """
    Execute Feature 2 as a standalone step.
    """
    print(f"Starting HTML parsing from: {input_path}")

    try:
        soup = parse_webpage(input_path)
        summary = summarize_document(soup)

        print("HTML parsed successfully.")
        print(f"Document title: {soup.title.get_text(strip=True) if soup.title else 'N/A'}")
        print(f"Headings found: {summary['headings']}")
        print(f"Paragraphs found: {summary['paragraphs']}")
        print(f"Links found: {summary['links']}")
        print(f"Code blocks found: {summary['code_blocks']}")
        return soup

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error while parsing HTML: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BeautifulSoup HTML Parser")
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_PATH,
        help="Path to the raw HTML file to parse",
    )

    args = parser.parse_args()
    parsed = run_parser(args.input)
    if parsed is None:
        raise SystemExit(1)
