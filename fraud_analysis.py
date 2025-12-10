"""
Fraud Analysis Module
Performs NLP analysis on banking articles to identify fraud patterns, 
sentiment, and risk levels.
"""

import pandas as pd
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings('ignore')

# Fraud category keywords
FRAUD_CATEGORIES = {
    'Check Fraud': ['check fraud', 'forged check', 'counterfeit check', 'altered check', 'fake check'],
    'Wire Fraud': ['wire fraud', 'wire transfer fraud', 'ach fraud', 'electronic transfer fraud'],
    'Identity Theft': ['identity theft', 'synthetic identity', 'stolen identity', 'identity fraud', 
                       'account takeover', 'impersonation'],
    'Credit Card Fraud': ['credit card fraud', 'card fraud', 'card not present', 'skimming', 
                          'card cloning', 'compromised card'],
    'Cyber Crime': ['cyber attack', 'cyberattack', 'hacking', 'ransomware', 'malware', 
                    'phishing', 'data breach', 'security breach', 'ddos'],
    'Money Laundering': ['money laundering', 'aml', 'anti-money laundering', 'suspicious activity',
                         'sar', 'structuring', 'smurfing', 'layering'],
    'Embezzlement': ['embezzlement', 'employee theft', 'internal fraud', 'misappropriation'],
    'Regulatory Compliance': ['compliance', 'regulation', 'bsa', 'bank secrecy act', 'kyc',
                             'know your customer', 'fincen', 'sanctions', 'ofac'],
    'Other Financial Crime': ['fraud', 'scam', 'fraudulent', 'financial crime', 'deepfake']
}

# Risk level indicators
HIGH_RISK_KEYWORDS = ['major breach', 'significant loss', 'millions', 'billions', 'widespread', 
                      'severe', 'massive', 'systemic', 'enforcement action', 
                      'criminal charges', 'indictment', 'prosecution', 'fine', 'penalty']

MEDIUM_RISK_KEYWORDS = ['warning', 'alert', 'concern', 'investigation', 'suspected', 'potential',
                        'vulnerability', 'thousands', 'settlement', 'critical']

LOW_RISK_KEYWORDS = ['prevention', 'protection', 'security measure', 'update', 'patch',
                     'awareness', 'training', 'advisory', 'guidance', 'best practice']


def download_nltk_resources():
    """Download required NLTK resources if not already present."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords', quiet=True)


def categorize_fraud_type(text):
    """
    Categorize the type of fraud based on keywords in the text.
    
    Args:
        text (str): Article text to analyze
    
    Returns:
        list: List of fraud categories found
    """
    if not text:
        return []
    
    text_lower = text.lower()
    categories_found = []
    
    for category, keywords in FRAUD_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                categories_found.append(category)
                break  # Only add category once even if multiple keywords match
    
    return categories_found if categories_found else ['Uncategorized']


def assess_risk_level(text):
    """
    Assess the risk level of fraud mentioned in the article.
    
    Args:
        text (str): Article text to analyze
    
    Returns:
        str: Risk level (High, Medium, Low, Unknown)
    """
    if not text:
        return 'Unknown'
    
    text_lower = text.lower()
    
    high_score = sum(1 for keyword in HIGH_RISK_KEYWORDS if keyword.lower() in text_lower)
    medium_score = sum(1 for keyword in MEDIUM_RISK_KEYWORDS if keyword.lower() in text_lower)
    low_score = sum(1 for keyword in LOW_RISK_KEYWORDS if keyword.lower() in text_lower)
    
    if high_score >= 2:
        return 'High'
    elif high_score >= 1 or medium_score >= 3:
        return 'Medium-High'
    elif medium_score >= 1:
        return 'Medium'
    elif low_score >= 1:
        return 'Low'
    else:
        return 'Unknown'


def extract_keywords(text, top_n=10):
    """
    Extract top keywords from text using frequency analysis.
    
    Args:
        text (str): Text to analyze
        top_n (int): Number of top keywords to return
    
    Returns:
        list: List of (keyword, frequency) tuples
    """
    if not text:
        return []
    
    # Tokenize and clean
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    try:
        stop_words = set(stopwords.words('english'))
    except:
        download_nltk_resources()
        stop_words = set(stopwords.words('english'))
    
    # Add custom stopwords
    custom_stopwords = {'said', 'say', 'says', 'also', 'would', 'could', 'one', 'two', 'three'}
    stop_words.update(custom_stopwords)
    
    keywords = [word for word in tokens if word.isalpha() and len(word) > 3 and word not in stop_words]
    
    # Count frequency
    keyword_freq = Counter(keywords)
    
    return keyword_freq.most_common(top_n)


def analyze_sentiment(text):
    """
    Simple sentiment analysis based on positive/negative keywords.
    
    Args:
        text (str): Text to analyze
    
    Returns:
        str: Sentiment (Negative, Neutral, Positive)
    """
    if not text:
        return 'Neutral'
    
    text_lower = text.lower()
    
    # Negative indicators for fraud context
    negative_words = ['breach', 'attack', 'fraud', 'theft', 'scam', 'loss', 'victim', 
                     'criminal', 'illegal', 'stolen', 'compromised', 'vulnerable',
                     'fine', 'penalty', 'violation', 'failure', 'concern', 'warning']
    
    # Positive indicators (protective measures, success)
    positive_words = ['prevention', 'protection', 'secure', 'success', 'improvement',
                     'enhance', 'strengthen', 'detect', 'recover', 'safeguard']
    
    negative_score = sum(1 for word in negative_words if word in text_lower)
    positive_score = sum(1 for word in positive_words if word in text_lower)
    
    if negative_score > positive_score + 2:
        return 'Negative'
    elif positive_score > negative_score + 1:
        return 'Positive'
    else:
        return 'Neutral'


def analyze_articles(csv_file):
    """
    Perform comprehensive fraud analysis on articles from CSV.
    
    Args:
        csv_file (str): Path to CSV file with articles
    
    Returns:
        pd.DataFrame: Enhanced dataframe with analysis results
    """
    print(f"\n{'='*60}")
    print(f"FRAUD ANALYSIS PIPELINE")
    print(f"{'='*60}\n")
    
    # Download NLTK resources
    download_nltk_resources()
    
    # Load data
    print("[LOAD] Loading articles...")
    df = pd.read_csv(csv_file)
    print(f"   Loaded {len(df)} articles")
    
    # Create combined text for analysis
    df['analysis_text'] = df['title'].fillna('') + ' ' + df['summary'].fillna('') + ' ' + df['full_content'].fillna('')
    
    print("\n[CATEGORIZE] Categorizing fraud types...")
    df['fraud_categories'] = df['analysis_text'].apply(categorize_fraud_type)
    df['fraud_categories_str'] = df['fraud_categories'].apply(lambda x: ', '.join(x))
    
    print("[RISK] Assessing risk levels...")
    df['risk_level'] = df['analysis_text'].apply(assess_risk_level)
    
    print("[SENTIMENT] Analyzing sentiment...")
    df['sentiment'] = df['analysis_text'].apply(analyze_sentiment)
    
    print("[KEYWORDS] Extracting keywords...")
    df['top_keywords'] = df['analysis_text'].apply(lambda x: ', '.join([kw[0] for kw in extract_keywords(x, 5)]))
    
    # Statistics
    print(f"\n{'='*60}")
    print(f"ANALYSIS RESULTS")
    print(f"{'='*60}\n")
    
    print("Fraud Category Distribution:")
    all_categories = []
    for cats in df['fraud_categories']:
        all_categories.extend(cats)
    cat_counts = Counter(all_categories)
    for cat, count in cat_counts.most_common():
        print(f"  {cat}: {count}")
    
    print("\nRisk Level Distribution:")
    print(df['risk_level'].value_counts().to_string())
    
    print("\nSentiment Distribution:")
    print(df['sentiment'].value_counts().to_string())
    
    return df


def save_analysis(df, output_file='fraud_analysis_results.csv'):
    """
    Save analyzed data to CSV.
    
    Args:
        df (pd.DataFrame): Analyzed dataframe
        output_file (str): Output file path
    """
    # Select relevant columns
    output_cols = ['title', 'date', 'url', 'summary', 'fraud_categories_str', 
                   'risk_level', 'sentiment', 'top_keywords', 'fraud_keywords']
    
    df[output_cols].to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n[SUCCESS] Analysis saved to: {output_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'fraud_articles.csv'
    
    # Run analysis
    analyzed_df = analyze_articles(input_file)
    
    # Save results
    save_analysis(analyzed_df)
    
    print(f"\n{'='*60}")
    print("Analysis complete!")
    print(f"{'='*60}\n")
