# QUICK START GUIDE - USAA Fraud Research Project

## Fast Setup (5 minutes)

### 1. Install Dependencies
```bash
cd "/Users/abhiv/DTSC USAA Project/Studio3USAA"
pip install -r requirements.txt
```

### 2. Run Complete Pipeline (Easiest!)
```bash
python run_pipeline.py
```
This runs everything: scraping → analysis → dashboard

---

## Or Run Steps Individually

### Option A: Default (20 fraud articles)
```bash
python BankingDiveWS.py                    # Scrape
python fraud_analysis.py                   # Analyze  
python fraud_dashboard.py                  # Visualize
open fraud_dashboard.html                  # View
```

### Option B: Custom (50 fraud articles)
```bash
python BankingDiveWS.py --num 50
python fraud_analysis.py
python fraud_dashboard.py
open fraud_dashboard.html
```

### Option C: All articles (not just fraud)
```bash
python BankingDiveWS.py --num 30 --all
python fraud_analysis.py
python fraud_dashboard.py
open fraud_dashboard.html
```

---

## What You Get

After running the pipeline, you'll have:

- **fraud_articles.csv** - Scraped articles with:
   - Title, summary, URL, date
   - Full article content
   - Fraud keywords identified

- **fraud_analysis_results.csv** - Analysis with:
   - Fraud categories (check fraud, wire fraud, etc.)
   - Risk levels (High/Medium/Low)
   - Sentiment analysis
   - Top keywords

- **fraud_dashboard.html** - Interactive visualizations:
   - Fraud category distribution
   - Risk level breakdown
   - Sentiment analysis
   - Keyword frequency
   - Timeline trends

- **fraud_summary_report.txt** - Text summary of findings

---

## Troubleshooting

**Issue**: Missing NLTK data
**Fix**: 
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

**Issue**: No fraud articles found
**Fix**: Try collecting more articles or use `--all` flag

**Issue**: ImportError for plotly/pandas
**Fix**: 
```bash
pip install --upgrade -r requirements.txt
```

---

## Pro Tips

1. **Start small**: Test with 10-20 articles first
2. **Fraud-only mode**: Faster and more relevant results
3. **Save your work**: CSV files can be reanalyzed without re-scraping
4. **Custom keywords**: Edit FRAUD_KEYWORDS list in fraud_analysis.py
5. **Export charts**: Right-click charts in dashboard to save as PNG

---

## Project Checklist

For your final submission, make sure you have:

- [ ] Collected sufficient articles (recommended: 50+ fraud-related)
- [ ] Generated fraud_analysis_results.csv
- [ ] Created interactive dashboard (fraud_dashboard.html)
- [ ] Reviewed summary report
- [ ] Documented any interesting findings
- [ ] Tested all visualizations work
- [ ] Prepared presentation slides (use dashboard screenshots)

---

## For Your Presentation

Key talking points from the analysis:

1. **Data Collection**: How many articles, time period, source
2. **Fraud Categories**: Most common types detected
3. **Risk Trends**: Distribution of risk levels
4. **Insights**: Notable patterns or findings
5. **Methodology**: NLP techniques used
6. **Visualizations**: Show interactive dashboard

---

Need help? Check README.md for full documentation!
