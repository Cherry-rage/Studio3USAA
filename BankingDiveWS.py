import requests
from bs4 import BeautifulSoup
import sys
import argparse
import csv
from datetime import datetime
import time
import re


# Fraud-related keywords to identify relevant articles
FRAUD_KEYWORDS = [
    'fraud', 'scam', 'fraudulent', 'cybercrime', 'cyber attack', 'data breach',
    'identity theft', 'phishing', 'money laundering', 'aml', 'kyc',
    'wire fraud', 'check fraud', 'credit card fraud', 'account takeover',
    'synthetic identity', 'deepfake', 'ransomware', 'hack', 'breach',
    'security breach', 'financial crime', 'embezzlement', 'bsa', 
    'bank secrecy act', 'suspicious activity', 'sar', 'fincen',
    'risk management', 'compliance', 'regulation', 'sanctions'
]


def contains_fraud_keywords(text, keywords=FRAUD_KEYWORDS):
    """
    Check if text contains any fraud-related keywords.
    
    Args:
        text (str): Text to search
        keywords (list): List of keywords to search for
    
    Returns:
        tuple: (bool, list) - Whether fraud keywords found and list of matched keywords
    """
    if not text:
        return False, []
    
    text_lower = text.lower()
    matched_keywords = []
    
    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched_keywords.append(keyword)
    
    return len(matched_keywords) > 0, matched_keywords


def scrape_full_article(article_url, headers):
    """
    Scrape the full content of an individual article.
    
    Args:
        article_url (str): URL of the article
        headers (dict): HTTP headers for the request
    
    Returns:
        str: Full article text or empty string if failed
    """
    try:
        time.sleep(1)  # Be polite to the server
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Banking Dive typically uses article body with specific classes
        article_body = soup.find('div', class_='article-body')
        if not article_body:
            article_body = soup.find('div', class_='content-body')
        
        if article_body:
            # Extract all paragraph text
            paragraphs = article_body.find_all('p')
            full_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            return full_text
        
        return ""
    except Exception as e:
        print(f"  Warning: Could not scrape full article from {article_url}: {e}")
        return ""


def scrape_banking_dive(num_articles=20, fraud_only=True):
    """
    Scrapes articles from Banking Dive with fraud detection and full content.

    Args:
        num_articles (int): The target number of articles to collect.
        fraud_only (bool): If True, only collect fraud-related articles.
    """
    
    base_url = "https://www.bankingdive.com/"
    articles_data = []
    page_num = 1
    
    # Set a User-Agent header to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Starting scraper... targeting {num_articles} articles.\n")

    seen_urls = set()

    try:
        # Loop through pages until we have enough articles
        while len(articles_data) < num_articles:
            # Construct the URL for the current page
            current_url = f"{base_url}?page={page_num}"
            print(f"Fetching page: {current_url}")
            
            time.sleep(1) # Add delay to avoid rate limiting
            
            # Make the HTTP request
            response = requests.get(current_url, headers=headers)
            
            # Check for bad responses (404, 403, 500, etc.)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all article items in the feed
            articles = soup.find_all('li', class_='row feed__item')
            
            # Filter out advertisement items
            articles = [article for article in articles if 'feed-item-ad' not in article.get('class', [])]

            # If no candidate articles found, assume we've reached the end
            if not articles:
                print("Found no article-like elements on this page. Stopping.")
                break

            # Loop through each article and extract data
            for article in articles:
                # Find the title in h3 with class 'feed__title'
                title_element = article.find('h3', class_='feed__title')
                if title_element:
                    title_link = title_element.find('a')  # Get the link containing the title
                else:
                    title_link = None
                
                # Find the summary paragraph with class 'feed__description'
                summary_element = article.find('p', class_='feed__description')
                
                # Find the date element - Search results use 'secondary-label' with "Posted:" text
                date_element = article.find('span', class_='secondary-label')
                if not date_element:
                    # Fallback for standard feed
                    date_element = article.find('span', class_='feed__date')

                # If we found required elements, process the article
                if title_link:
                    title = title_link.get_text(strip=True)
                    summary = summary_element.get_text(strip=True) if summary_element else ""
                    article_url = title_link.get('href', '')
                    
                    # Make URL absolute if it's relative
                    if article_url and not article_url.startswith('http'):
                        article_url = f"https://www.bankingdive.com{article_url}"
                    
                    # Check for duplicates
                    if article_url in seen_urls:
                        continue
                    seen_urls.add(article_url)

                    # Extract date
                    article_date = ""
                    if date_element:
                        date_text = date_element.get_text(strip=True)
                        # Clean up "Posted:" prefix if present
                        article_date = date_text.replace('Posted:', '').strip()
                    
                    # Check for fraud keywords
                    combined_text = f"{title} {summary}"
                    is_fraud_related, matched_keywords = contains_fraud_keywords(combined_text)
                    
                    # Skip if fraud_only is True and article is not fraud-related
                    if fraud_only and not is_fraud_related:
                        continue
                    
                    # Scrape full article content if fraud-related
                    full_content = ""
                    if is_fraud_related and article_url:
                        print(f"  [FRAUD] Fraud-related article found: {title[:60]}...")
                        print(f"     Keywords: {', '.join(matched_keywords[:5])}")
                        full_content = scrape_full_article(article_url, headers)
                    
                    articles_data.append({
                        'title': title,
                        'summary': summary,
                        'url': article_url,
                        'date': article_date,
                        'full_content': full_content,
                        'fraud_keywords': ', '.join(matched_keywords),
                        'is_fraud_related': is_fraud_related
                    })

                    # Stop once we've hit our target
                    if len(articles_data) >= num_articles:
                        break
            
            # Go to the next page
            # Go to the next page
            page_num += 1

            if page_num > 200:
                print("Reached page limit (200). Stopping.")
                break
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # --- Return the final results ---
    print(f"\n--- Successfully collected {len(articles_data)} articles ---")
    return articles_data

# --- How to Run This Code ---
# 1. Make sure you have the required libraries:
#    pip install requests
#    pip install beautifulsoup4
#
# 2. Save the code as a .py file (e.g., scraper.py)
# 3. Run it from your terminal:
def main(argv=None):
    parser = argparse.ArgumentParser(description='Scrape Banking Dive news with fraud detection.')
    parser.add_argument('--num', '-n', type=int, default=5000, help='Number of articles to collect (default: 5000)')
    parser.add_argument('--csv', '-o', type=str, default=None, help='Path to CSV output file (optional)')
    parser.add_argument('--all', '-a', action='store_true', help='Collect all articles, not just fraud-related')
    args = parser.parse_args(argv)

    fraud_only = not args.all
    articles = scrape_banking_dive(args.num, fraud_only=fraud_only)

    # Print summary statistics
    fraud_count = sum(1 for a in articles if a.get('is_fraud_related', False))
    print(f"\n{'='*60}")
    print(f"COLLECTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total articles collected: {len(articles)}")
    print(f"Fraud-related articles: {fraud_count}")
    print(f"Articles with full content: {sum(1 for a in articles if a.get('full_content'))}")
    
    # Print sample articles
    print(f"\n{'='*60}")
    print(f"SAMPLE ARTICLES")
    print(f"{'='*60}")
    for i, article in enumerate(articles[:5]):
        print(f"\nARTICLE {i + 1}")
        print(f"  Title: {article['title'][:80]}...")
        print(f"  Date: {article.get('date', 'N/A')}")
        print(f"  Fraud-Related: {'Yes' if article.get('is_fraud_related') else 'No'}")
        if article.get('fraud_keywords'):
            print(f"  Keywords: {article['fraud_keywords'][:100]}")
        print(f"  URL: {article.get('url', 'N/A')[:80]}...")

    # Always write to articles.csv in the current directory if no CSV path specified
    output_file = args.csv if args.csv else 'fraud_articles.csv'
    
    try:
        # Use UTF-8-sig so Excel on Windows can read the UTF-8 CSV correctly
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['title', 'summary', 'url', 'date', 'fraud_keywords', 
                         'is_fraud_related', 'full_content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for article in articles[:args.num]:
                # Clean the data to remove any potential CSV-breaking characters
                clean_article = {}
                for key, value in article.items():
                    if isinstance(value, str):
                        clean_article[key] = value.replace('\n', ' ').replace('\r', '')
                    else:
                        clean_article[key] = value
                writer.writerow(clean_article)
        print(f"\n[SUCCESS] Successfully wrote {len(articles[:args.num])} articles to: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to write CSV {output_file}: {e}")
        print("Error details:", str(e))


if __name__ == "__main__":
    main()
