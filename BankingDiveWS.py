import requests
from bs4 import BeautifulSoup
import sys
import argparse
import csv


def scrape_banking_dive(num_articles=20):
    """
    Scrapes the titles and summaries of articles from Banking Dive.

    Args:
        num_articles (int): The target number of articles to collect.
    """
    
    base_url = "https://www.bankingdive.com/news/"
    articles_data = []
    page_num = 1
    
    # Set a User-Agent header to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Starting scraper... targeting {num_articles} articles.\n")

    try:
        # Loop through pages until we have enough articles
        while len(articles_data) < num_articles:
            # Construct the URL for the current page
            # page=1 is the same as the main /news/ page
            current_url = f"{base_url}?page={page_num}"
            print(f"Fetching page: {current_url}")
            
            # Make the HTTP request
            response = requests.get(current_url, headers=headers)
            
            # Check for bad responses (404, 403, 500, etc.)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # New strategy: Banking Dive may use containers with classes that include
            # 'rowfeed' (for example rowfeed items). Search for any elements whose
            # class contains the substring 'rowfeed' and treat each as an article
            # candidate. This is more robust than relying on a single <ul> wrapper.
            # Removed the has_feed_class helper function as it's no longer needed

            # Find all article items in the feed
            articles = soup.find_all('li', class_='row feed__item')
            
            # Filter out advertisement items
            articles = [article for article in articles if 'feed-item-ad' not in article.get('class', [])]

            # If no candidate articles found, assume we've reached the end
            if not articles:
                print("Found no article-like elements on this page. Stopping.")
                break

            # Loop through each article and extract title and summary
            for article in articles:
                # Find the title in h3 with class 'feed__title'
                title_element = article.find('h3', class_='feed__title')
                if title_element:
                    title_element = title_element.find('a')  # Get the link containing the title
                
                # Find the summary paragraph with class 'feed__description'
                summary_element = article.find('p', class_='feed__description')

                # If we found both elements, add them to our data
                if title_element and summary_element:
                    title = title_element.get_text(strip=True)
                    summary = summary_element.get_text(strip=True)
                    articles_data.append({'title': title, 'summary': summary})

                    # Stop once we've hit our target
                    if len(articles_data) >= num_articles:
                        break
            
            # Go to the next page
            page_num += 1

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
#    python scraper.py

def main(argv=None):
    parser = argparse.ArgumentParser(description='Scrape Banking Dive news titles and summaries.')
    parser.add_argument('--num', '-n', type=int, default=20, help='Number of articles to collect (default: 20)')
    parser.add_argument('--csv', '-o', type=str, default=None, help='Path to CSV output file (optional)')
    args = parser.parse_args(argv)

    articles = scrape_banking_dive(args.num)

    # Print to stdout (trimmed) like before
    for i, article in enumerate(articles[:args.num]):
        print(f"\nARTICLE {i + 1}")
        print(f"  Title: {article['title']}")
        print(f"  Summary: {article['summary']}")

    # Always write to articles.csv in the current directory if no CSV path specified
    output_file = args.csv if args.csv else 'articles.csv'
    
    try:
        # Use UTF-8-sig so Excel on Windows can read the UTF-8 CSV correctly
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'summary'])
            writer.writeheader()
            for article in articles[:args.num]:
                # Clean the data to remove any potential CSV-breaking characters
                clean_title = article['title'].replace('\n', ' ').replace('\r', '')
                clean_summary = article['summary'].replace('\n', ' ').replace('\r', '')
                writer.writerow({
                    'title': clean_title,
                    'summary': clean_summary
                })
        print(f"\nWrote {len(articles[:args.num])} articles to CSV: {output_file}")
    except Exception as e:
        print(f"Failed to write CSV {output_file}: {e}")
        print("Error details:", str(e))


if __name__ == "__main__":
    main()
