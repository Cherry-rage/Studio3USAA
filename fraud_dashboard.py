"""
Fraud Dashboard - Interactive visualization of fraud trends and patterns
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def load_data(csv_file='fraud_analysis_results.csv'):
    """Load analyzed fraud data."""
    try:
        df = pd.read_csv(csv_file)
        print(f"[SUCCESS] Loaded {len(df)} articles from {csv_file}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] File not found: {csv_file}")
        print("   Please run fraud_analysis.py first to generate the analysis results.")
        return None


def create_fraud_category_chart(df):
    """Create bar chart of fraud categories."""
    # Parse fraud categories
    all_categories = []
    for cats in df['fraud_categories_str'].dropna():
        all_categories.extend([c.strip() for c in cats.split(',')])
    
    cat_counts = pd.Series(all_categories).value_counts()
    
    fig = px.bar(
        x=cat_counts.values,
        y=cat_counts.index,
        orientation='h',
        title='Fraud Categories Distribution',
        labels={'x': 'Number of Articles', 'y': 'Fraud Category'}
    )
    
    # Professional navy blue color scheme
    fig.update_traces(marker_color='#2C3E50')
    
    fig.update_layout(
        showlegend=False,
        height=500,
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2C3E50')
    )
    
    return fig


def create_risk_level_chart(df):
    """Create pie chart of risk levels."""
    risk_counts = df['risk_level'].value_counts()
    
    # Professional graduated color scheme - dark to light grays/blues
    colors = {
        'High': '#34495E',        # Dark slate blue
        'Medium-High': '#5D6D7E', # Medium slate
        'Medium': '#85929E',      # Light slate
        'Low': '#AEB6BF',         # Very light slate
        'Unknown': '#D5D8DC'      # Almost white gray
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=[colors.get(level, '#D5D8DC') for level in risk_counts.index]),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Risk Level Distribution',
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2C3E50')
    )
    
    return fig


def create_sentiment_chart(df):
    """Create sentiment analysis visualization."""
    sentiment_counts = df['sentiment'].value_counts()
    
    # Professional monochromatic color scheme
    colors = {
        'Positive': '#7F8C8D',  # Medium gray
        'Neutral': '#95A5A6',   # Light gray
        'Negative': '#34495E'   # Dark blue-gray
    }
    
    fig = px.bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        title='Sentiment Analysis of Fraud Articles',
        labels={'x': 'Sentiment', 'y': 'Number of Articles'},
        color=sentiment_counts.index,
        color_discrete_map=colors
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2C3E50')
    )
    
    return fig


def create_trend_timeline(df):
    """Create timeline of articles if dates are available."""
    if 'date' not in df.columns or df['date'].isna().all():
        return None
    
    # Try to parse dates
    df_copy = df.copy()
    df_copy['parsed_date'] = pd.to_datetime(df_copy['date'], errors='coerce')
    df_valid = df_copy.dropna(subset=['parsed_date'])
    
    if len(df_valid) == 0:
        return None
    
    # Group by date
    timeline = df_valid.groupby(df_valid['parsed_date'].dt.date).size().reset_index()
    timeline.columns = ['Date', 'Articles']
    
    fig = px.line(
        timeline,
        x='Date',
        y='Articles',
        title='Fraud Articles Over Time',
        markers=True
    )
    
    # Professional line color
    fig.update_traces(line_color='#2C3E50', marker=dict(color='#2C3E50'))
    
    fig.update_layout(
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2C3E50')
    )
    
    return fig


def create_keyword_cloud_data(df):
    """Extract top keywords across all articles."""
    all_keywords = []
    
    for keywords in df['top_keywords'].dropna():
        all_keywords.extend([k.strip() for k in keywords.split(',')])
    
    keyword_counts = pd.Series(all_keywords).value_counts().head(20)
    
    return keyword_counts


def create_comprehensive_dashboard(csv_file='fraud_analysis_results.csv'):
    """Create and display comprehensive fraud dashboard."""
    print(f"\n{'='*60}")
    print(f"GENERATING FRAUD DASHBOARD")
    print(f"{'='*60}\n")
    
    df = load_data(csv_file)
    if df is None:
        return
    
    # Create visualizations
    print("[CHART] Creating fraud category chart...")
    fig1 = create_fraud_category_chart(df)
    fig1.write_html('fraud_categories_chart.html')
    
    print("[CHART] Creating risk level chart...")
    fig2 = create_risk_level_chart(df)
    fig2.write_html('risk_levels_chart.html')
    
    print("[CHART] Creating sentiment chart...")
    fig3 = create_sentiment_chart(df)
    fig3.write_html('sentiment_chart.html')
    
    print("[CHART] Creating timeline...")
    fig4 = create_trend_timeline(df)
    if fig4:
        fig4.write_html('fraud_timeline.html')
    
    # Create combined dashboard
    print("[CHART] Creating combined dashboard...")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Fraud Categories', 'Risk Levels', 
                       'Sentiment Analysis', 'Top Keywords'),
        specs=[[{'type': 'bar'}, {'type': 'pie'}],
               [{'type': 'bar'}, {'type': 'bar'}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Add fraud categories
    cat_fig = create_fraud_category_chart(df)
    for trace in cat_fig.data:
        fig.add_trace(trace, row=1, col=1)
    
    # Add risk levels
    risk_fig = create_risk_level_chart(df)
    for trace in risk_fig.data:
        fig.add_trace(trace, row=1, col=2)
    
    # Add sentiment
    sent_fig = create_sentiment_chart(df)
    for trace in sent_fig.data:
        fig.add_trace(trace, row=2, col=1)
    
    # Add keywords
    keywords = create_keyword_cloud_data(df)
    fig.add_trace(
        go.Bar(x=keywords.values, y=keywords.index, orientation='h',
               marker_color='#2C3E50'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=900,
        title_text="Fraud Analysis Dashboard - USAA Banking Project",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2C3E50', family='Arial, sans-serif', size=12)
    )
    
    fig.write_html('fraud_dashboard.html')
    
    # Generate summary report
    print("\n[REPORT] Generating summary report...")
    generate_summary_report(df)
    
    print(f"\n{'='*60}")
    print("DASHBOARD GENERATION COMPLETE")
    print(f"{'='*60}\n")
    print("Generated files:")
    print("  - fraud_dashboard.html - Complete interactive dashboard")
    print("  - fraud_categories_chart.html - Category breakdown")
    print("  - risk_levels_chart.html - Risk distribution")
    print("  - sentiment_chart.html - Sentiment analysis")
    if fig4:
        print("  - fraud_timeline.html - Article timeline")
    print("  - fraud_summary_report.txt - Text summary")
    print("\nOpen fraud_dashboard.html in your browser to view the interactive dashboard!")


def generate_summary_report(df):
    """Generate a text summary report."""
    with open('fraud_summary_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("FRAUD ANALYSIS SUMMARY REPORT\n")
        f.write("USAA Banking Industry Fraud Research Project\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"OVERVIEW\n")
        f.write("-"*70 + "\n")
        f.write(f"Total Articles Analyzed: {len(df)}\n")
        f.write(f"Fraud-Related Articles: {df['fraud_categories_str'].notna().sum()}\n\n")
        
        f.write(f"FRAUD CATEGORIES\n")
        f.write("-"*70 + "\n")
        all_categories = []
        for cats in df['fraud_categories_str'].dropna():
            all_categories.extend([c.strip() for c in cats.split(',')])
        cat_counts = pd.Series(all_categories).value_counts()
        for cat, count in cat_counts.items():
            f.write(f"  {cat}: {count} articles\n")
        
        f.write(f"\nRISK LEVEL DISTRIBUTION\n")
        f.write("-"*70 + "\n")
        for level, count in df['risk_level'].value_counts().items():
            f.write(f"  {level}: {count} articles\n")
        
        f.write(f"\nSENTIMENT ANALYSIS\n")
        f.write("-"*70 + "\n")
        for sentiment, count in df['sentiment'].value_counts().items():
            f.write(f"  {sentiment}: {count} articles\n")
        
        f.write(f"\nTOP 10 KEYWORDS\n")
        f.write("-"*70 + "\n")
        keywords = create_keyword_cloud_data(df)
        for i, (keyword, count) in enumerate(keywords.head(10).items(), 1):
            f.write(f"  {i}. {keyword}: {count} occurrences\n")
        
        f.write(f"\nHIGH-RISK ARTICLES\n")
        f.write("-"*70 + "\n")
        high_risk = df[df['risk_level'] == 'High']
        if len(high_risk) > 0:
            for idx, row in high_risk.iterrows():
                f.write(f"\n• {row['title']}\n")
                f.write(f"  Categories: {row.get('fraud_categories_str', 'N/A')}\n")
                f.write(f"  Date: {row.get('date', 'N/A')}\n")
        else:
            f.write("  No high-risk articles found.\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'fraud_analysis_results.csv'
    
    create_comprehensive_dashboard(input_file)
