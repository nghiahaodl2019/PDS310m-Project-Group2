import sys
from collector import collect_webpage
from parser import run_parser

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

if __name__ == "__main__":
    main()
