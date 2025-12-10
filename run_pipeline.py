#!/usr/bin/env python3
"""
Complete Pipeline Runner
Runs the entire fraud analysis pipeline from scraping to dashboard generation.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*70}")
    print(f"[RUN] {description}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, 
                              capture_output=False)
        print(f"\n[SUCCESS] {description} - COMPLETE")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {description} - FAILED")
        print(f"Error: {e}")
        return False


def main():
    """Run the complete pipeline."""
    print(f"\n{'*'*70}")
    print(f"{'*'*70}")
    print(f"  USAA FRAUD RESEARCH PIPELINE")
    print(f"  Complete End-to-End Analysis")
    print(f"{'*'*70}")
    print(f"{'*'*70}\n")
    
    # Get number of articles from user
    try:
        num_articles = input("How many articles would you like to collect? (default: 20): ").strip()
        if not num_articles:
            num_articles = "20"
        num_articles = int(num_articles)
    except ValueError:
        print("Invalid input. Using default of 20 articles.")
        num_articles = 20
    
    # Ask if fraud-only
    fraud_only = input("Collect fraud-related articles only? (Y/n): ").strip().lower()
    fraud_flag = "" if fraud_only in ['', 'y', 'yes'] else "--all"
    
    print(f"\nPipeline Configuration:")
    print(f"   Articles to collect: {num_articles}")
    print(f"   Mode: {'Fraud-only' if fraud_flag == '' else 'All articles'}")
    
    # Step 1: Scrape articles
    if not run_command(
        f"python3 BankingDiveWS.py --num {num_articles} {fraud_flag}",
        "STEP 1/3: Web Scraping"
    ):
        print("\n[WARNING] Pipeline stopped due to scraping error.")
        return
    
    # Step 2: Analyze articles
    if not run_command(
        "python3 fraud_analysis.py fraud_articles.csv",
        "STEP 2/3: NLP Analysis"
    ):
        print("\n[WARNING] Pipeline stopped due to analysis error.")
        return
    
    # Step 3: Generate dashboard
    if not run_command(
        "python3 fraud_dashboard.py fraud_analysis_results.csv",
        "STEP 3/3: Dashboard Generation"
    ):
        print("\n[WARNING] Pipeline stopped due to dashboard error.")
        return
    
    # Success!
    print(f"\n{'*'*70}")
    print(f"{'*'*70}")
    print(f"  PIPELINE COMPLETE!")
    print(f"{'*'*70}")
    print(f"{'*'*70}\n")
    
    print("Generated Files:")
    print("   - fraud_articles.csv - Raw scraped data")
    print("   - fraud_analysis_results.csv - Analysis results")
    print("   - fraud_dashboard.html - Interactive dashboard")
    print("   - fraud_summary_report.txt - Summary report")
    print("   - Individual chart HTML files\n")
    
    # Ask if user wants to open dashboard
    open_dashboard = input("Would you like to open the dashboard now? (Y/n): ").strip().lower()
    if open_dashboard in ['', 'y', 'yes']:
        print("\nOpening dashboard in browser...")
        if sys.platform == 'darwin':  # macOS
            os.system("open fraud_dashboard.html")
        elif sys.platform == 'win32':  # Windows
            os.system("start fraud_dashboard.html")
        else:  # Linux
            os.system("xdg-open fraud_dashboard.html")
    
    print("\nAll done! Happy analyzing!\n")


if __name__ == "__main__":
    main()
