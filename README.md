# USAA Fraud Research and Storytelling Project

A comprehensive data analysis project that scrapes, analyzes, and visualizes fraud trends in the banking industry using Banking Dive articles.

## Project Overview

This project collects banking news articles, identifies fraud-related content, performs NLP analysis, and creates interactive visualizations to tell a data-driven story about fraud trends in the financial industry.

## Features

- **Web Scraping**: Automated collection of banking news articles from Banking Dive
- **Fraud Detection**: Keyword-based identification of fraud-related content
- **Full Article Extraction**: Scrapes complete article text for in-depth analysis
- **NLP Analysis**:
  - Fraud categorization (check fraud, wire fraud, identity theft, etc.)
  - Risk level assessment (High, Medium, Low)
  - Sentiment analysis
  - Keyword extraction
- **Interactive Dashboards**: Plotly-based visualizations showing trends and patterns
- **Comprehensive Reporting**: Automated summary reports

## Project Structure

```
Studio3USAA/
├── BankingDiveWS.py          # Web scraper with fraud detection
├── fraud_analysis.py          # NLP analysis engine
├── fraud_dashboard.py         # Visualization dashboard generator
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── fraud_articles.csv         # Scraped articles (generated)
├── fraud_analysis_results.csv # Analysis results (generated)
└── fraud_dashboard.html       # Interactive dashboard (generated)
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   cd "/Users/abhiv/DTSC USAA Project/Studio3USAA"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (will happen automatically on first run):
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Usage

### Step 1: Scrape Articles

Collect fraud-related articles from Banking Dive:

```bash
# Collect 20 fraud-related articles (default)
python BankingDiveWS.py

# Collect 50 fraud-related articles
python BankingDiveWS.py --num 50

# Collect all articles (not just fraud-related)
python BankingDiveWS.py --num 30 --all

# Specify custom output file
python BankingDiveWS.py --csv my_articles.csv
```

**Output**: `fraud_articles.csv`

### Step 2: Analyze Articles

Perform NLP analysis on collected articles:

```bash
# Analyze default file (fraud_articles.csv)
python fraud_analysis.py

# Analyze custom file
python fraud_analysis.py my_articles.csv
```

**Output**: `fraud_analysis_results.csv`

### Step 3: Generate Dashboard

Create interactive visualizations:

```bash
# Generate dashboard from default file
python fraud_dashboard.py

# Generate from custom file
python fraud_dashboard.py my_analysis.csv
```

**Outputs**:
- `fraud_dashboard.html` - Complete interactive dashboard
- `fraud_categories_chart.html` - Category breakdown
- `risk_levels_chart.html` - Risk distribution
- `sentiment_chart.html` - Sentiment analysis
- `fraud_summary_report.txt` - Text summary

### Step 4: View Results

You can view the results in two ways:

**Option A: Streamlit App (Recommended)**
This provides a modern, interactive web application.
```bash
streamlit run streamlit_app.py
```

**Option B: Static HTML Dashboard**
Open the generated HTML files in your web browser:
```bash
open fraud_dashboard.html
```

## Fraud Categories Detected

- **Check Fraud**: Forged/counterfeit checks
- **Wire Fraud**: Electronic transfer fraud
- **Identity Theft**: Synthetic identity, account takeover
- **Credit Card Fraud**: Card cloning, skimming
- **Cyber Crime**: Hacking, ransomware, phishing, data breaches
- **Money Laundering**: AML violations, suspicious activity
- **Embezzlement**: Internal fraud, employee theft
- **Regulatory Compliance**: BSA, KYC, sanctions violations
- **Other Financial Crime**: General fraud and scams

## Risk Assessment Levels

- **High**: Major breaches, significant losses, criminal charges
- **Medium-High**: Investigations, enforcement actions, substantial concerns
- **Medium**: Warnings, alerts, potential vulnerabilities
- **Low**: Prevention measures, security updates, best practices
- **Unknown**: Insufficient information to assess risk

## Dashboard Features

The interactive dashboard includes:

1. **Fraud Category Distribution** - Bar chart showing frequency of each fraud type
2. **Risk Level Breakdown** - Pie chart of risk levels
3. **Sentiment Analysis** - Overall tone of fraud reporting
4. **Top Keywords** - Most frequently mentioned terms
5. **Timeline** - Fraud articles over time (if dates available)
6. **Summary Statistics** - Key metrics and insights

## Technical Details

### Web Scraping
- Uses BeautifulSoup for HTML parsing
- Implements polite scraping with delays
- Handles pagination automatically
- Extracts: title, summary, date, URL, full content

### NLP Analysis
- NLTK for tokenization and stopword removal
- Keyword frequency analysis
- Pattern matching for categorization
- Custom scoring for risk assessment

### Visualization
- Plotly for interactive charts
- Color-coded risk levels
- Responsive HTML dashboards
- Export-ready formats
