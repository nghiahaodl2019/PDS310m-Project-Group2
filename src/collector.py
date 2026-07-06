import os
import argparse
from pathlib import Path
import requests

# Resolve paths relative to the project root, not the current shell directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default configuration
DEFAULT_URL = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "beautifulsoup_doc.html"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

def collect_webpage(url: str = DEFAULT_URL, output_path: str = DEFAULT_OUTPUT_PATH) -> bool:
    """
    Downloads the HTML content of the target URL and saves it to output_path.
    
    Args:
        url (str): The target URL to download.
        output_path (str): The file path where the HTML content should be saved.
        
    Returns:
        bool: True if collection was successful, False otherwise.
    """
    print(f"Starting web collection from URL: {url}")
    headers = {"User-Agent": USER_AGENT}
    
    try:
        # Send HTTP GET request with a 20-second timeout
        response = requests.get(url, headers=headers, timeout=20)
        
        # Check HTTP status code
        print(f"HTTP Status Code: {response.status_code}")
        response.raise_for_status()
        
        html_content = response.text
        
        # Ensure the destination directory exists
        output_path = Path(output_path)
        output_dir = output_path.parent
        if not output_dir.exists():
            print(f"Creating directory: {output_dir}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
        # Save raw HTML into the destination file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Successfully saved raw HTML to: {output_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return False
    except IOError as e:
        print(f"Error saving file: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BeautifulSoup Doc Web Page Collector")
    parser.add_argument("--url", default=DEFAULT_URL, help="The target URL to download")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH, help="The destination path to save the HTML file")
    
    args = parser.parse_args()
    success = collect_webpage(url=args.url, output_path=args.output)
    if not success:
        exit(1)
