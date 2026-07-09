import sys
from collector import collect_webpage
from parser import run_parser
from src.extractor import run_all_extractions


def main():
    print("Starting BeautifulSoup Documentation Analytics System Pipeline...")
    
    # Feature 1: Web Page Collector
    print("\n--- Running Feature 1: Web Page Collector ---")
    success = collect_webpage()
    if not success:
        print("Feature 1: Web Page Collector failed. Exiting pipeline.")
        sys.exit(1)

    # Feature 2: HTML Parser
    print("\n--- Running Feature 2: HTML Parser ---")
    parsed_soup = run_parser()
    if parsed_soup is None:
        print("Feature 2: HTML Parser failed. Exiting pipeline.")
        sys.exit(1)

    print("\nPipeline executed successfully up to Feature 2.")


    # Features 3, 4, 5: Section, Link, and Code Example Extractor
    print("\n--- Running Features 3, 4, 5: Extractor ---")
    extraction_results = run_all_extractions()
    if extraction_results is None:
        print("Features 3, 4, 5: Extractor failed. Exiting pipeline.")
        sys.exit(1)

    print("\nPipeline executed successfully up to Feature 5.")
    print("Check the 'data/processed/' directory for the generated CSV files.")

if __name__ == "__main__":
    main()
