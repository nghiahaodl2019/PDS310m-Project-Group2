import sys
from collector import collect_webpage
from parser import run_parser
from extractor import run_all_extractions
from analyzer import run_all_analytics
from visualizer import run_all_visualizations
from report_generator import run_report_generator


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

    # Feature 6: Documentation Analytics
    print("\n--- Running Feature 6: Documentation Analytics ---")
    analysis_results = run_all_analytics(extraction_results)
    if analysis_results is None:
        print("Feature 6: Documentation Analytics failed. Exiting pipeline.")
        sys.exit(1)

    print("\nPipeline executed successfully up to Feature 6.")
    print("Check 'output/analysis_results.json' and 'output/summary_tables.xlsx'.")

    # Feature 7: Data Visualization
    print("\n--- Running Feature 7: Data Visualization ---")
    chart_results = run_all_visualizations(extraction_results)
    if chart_results is None:
        print("Feature 7: Data Visualization failed. Exiting pipeline.")
        sys.exit(1)

    print("\nPipeline executed successfully up to Feature 7.")
    print("Check the 'output/charts/' directory for the generated chart images.")

    # Feature 8: Final Report Generator
    print("\n--- Running Feature 8: Final Report Generator ---")
    report_path = run_report_generator(analysis_results)
    if report_path is None:
        print("Feature 8: Final Report Generator failed. Exiting pipeline.")
        sys.exit(1)

    print("\nPipeline executed successfully up to Feature 8.")
    print(f"Final report generated at: {report_path}")

if __name__ == "__main__":
    main()
