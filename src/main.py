import sys
from collector import collect_webpage

def main():
    print("Starting BeautifulSoup Documentation Analytics System Pipeline...")
    
    # Feature 1: Web Page Collector
    print("\n--- Running Feature 1: Web Page Collector ---")
    success = collect_webpage()
    if not success:
        print("Feature 1: Web Page Collector failed. Exiting pipeline.")
        sys.exit(1)
        
    print("\nPipeline executed successfully up to Feature 1.")

if __name__ == "__main__":
    main()
