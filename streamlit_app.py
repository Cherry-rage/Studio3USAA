import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="USAA Fraud Analysis Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stApp {
        background-color: #0E1117;
    }
    h1, h2, h3, p, div, span {
        color: #FAFAFA !important;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.5);
        text-align: center;
    }
    /* Fix for metric values */
    [data-testid="stMetricValue"] {
        color: #FAFAFA !important;
    }
    [data-testid="stMetricLabel"] {
        color: #FAFAFA !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data(csv_file='fraud_analysis_results.csv'):
    """Load and cache the analyzed data."""
    try:
        df = pd.read_csv(csv_file)
        # Convert date to datetime
        df['parsed_date'] = pd.to_datetime(df['date'], errors='coerce')
        return df
    except FileNotFoundError:
        return None

def create_fraud_category_chart(df):
    """Create bar chart of fraud categories."""
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
    fig.update_traces(marker_color='#3498DB')
    fig.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font=dict(color='#FAFAFA'))
    return fig

def create_risk_level_chart(df):
    """Create pie chart of risk levels."""
    # Rename 'Unknown' to 'No Fraud Detected' for visualization
    df_chart = df.copy()
    df_chart['risk_level'] = df_chart['risk_level'].replace('Unknown', 'No Fraud Detected')
    
    risk_counts = df_chart['risk_level'].value_counts()
    
    colors = {
        'High': '#34495E',        # Dark slate blue
        'Medium-High': '#5D6D7E', # Medium slate
        'Medium': '#85929E',      # Light slate
        'Low': '#AEB6BF',         # Very light slate
        'No Fraud Detected': '#D5D8DC'      # Almost white gray (was Unknown)
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=[colors.get(level, '#D5D8DC') for level in risk_counts.index]),
        hole=0.4
    )])
    fig.update_layout(title='Risk Level Distribution', plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font=dict(color='#FAFAFA'))
    return fig

def create_sentiment_chart(df):
    """Create sentiment analysis chart."""
    sentiment_counts = df['sentiment'].value_counts()
    colors = {'Positive': '#7F8C8D', 'Neutral': '#95A5A6', 'Negative': '#34495E'}
    
    fig = px.bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        title='Sentiment Analysis',
        color=sentiment_counts.index,
        color_discrete_map=colors
    )
    fig.update_layout(showlegend=False, plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font=dict(color='#FAFAFA'))
    return fig

def create_timeline(df):
    """Create timeline chart."""
    if 'parsed_date' not in df.columns or df['parsed_date'].isna().all():
        return None
        
    timeline = df.dropna(subset=['parsed_date']).groupby(df['parsed_date'].dt.date).size().reset_index()
    timeline.columns = ['Date', 'Articles']
    
    fig = px.line(timeline, x='Date', y='Articles', title='Fraud Articles Over Time', markers=True)
    fig.update_traces(line_color='#3498DB', marker=dict(color='#3498DB'))
    fig.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font=dict(color='#FAFAFA'))
    return fig

def main():
    # Sidebar
    st.sidebar.title("⚙️ Controls")
    st.sidebar.info("This dashboard visualizes fraud trends from banking news articles.")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ Data file 'fraud_analysis_results.csv' not found.")
        st.warning("Please run the pipeline first: `python run_pipeline.py`")
        return

    # Sidebar filters
    st.sidebar.subheader("Filters")
    
    # Risk Level Filter
    all_risks = ['All'] + sorted(df['risk_level'].unique().tolist())
    selected_risk = st.sidebar.selectbox("Risk Level", all_risks)
    
    # Category Filter
    all_cats = set()
    for cats in df['fraud_categories_str'].dropna():
        all_cats.update([c.strip() for c in cats.split(',')])
    all_cats = ['All'] + sorted(list(all_cats))
    selected_cat = st.sidebar.selectbox("Fraud Category", all_cats)

    # Apply filters
    filtered_df = df.copy()
    if selected_risk != 'All':
        filtered_df = filtered_df[filtered_df['risk_level'] == selected_risk]
    if selected_cat != 'All':
        filtered_df = filtered_df[filtered_df['fraud_categories_str'].str.contains(selected_cat, na=False)]

    # Main Content
    st.title("🛡️ USAA Fraud Intelligence Dashboard")
    st.markdown(f"Analyzing **{len(filtered_df)}** articles for fraud patterns and risks.")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Articles", len(filtered_df))
    with col2:
        high_risk_count = len(filtered_df[filtered_df['risk_level'] == 'High'])
        st.metric("High Risk Alerts", high_risk_count, delta_color="inverse")
    with col3:
        fraud_count = filtered_df['fraud_categories_str'].notna().sum()
        st.metric("Fraud Related", fraud_count)
    with col4:
        latest_date = filtered_df['parsed_date'].max()
        date_str = latest_date.strftime('%Y-%m-%d') if pd.notna(latest_date) else "N/A"
        st.metric("Latest Update", date_str)

    st.markdown("---")

    # Charts Row 1
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.plotly_chart(create_fraud_category_chart(filtered_df), use_container_width=True)
    
    with col_right:
        st.plotly_chart(create_risk_level_chart(filtered_df), use_container_width=True)

    # Charts Row 2
    col_left_2, col_right_2 = st.columns(2)
    
    with col_left_2:
        st.plotly_chart(create_sentiment_chart(filtered_df), use_container_width=True)
        
    with col_right_2:
        timeline_fig = create_timeline(filtered_df)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
        # Removed the else block to hide the message

    # High Risk Articles Section
    st.markdown("### 🚨 High Priority Alerts")
    high_risk_df = filtered_df[filtered_df['risk_level'] == 'High'].head(5)
    
    if not high_risk_df.empty:
        for _, row in high_risk_df.iterrows():
            with st.expander(f"🔴 {row['title']}"):
                st.markdown(f"**Date:** {row['date']}")
                st.markdown(f"**Categories:** {row['fraud_categories_str']}")
                st.markdown(f"**Summary:** {row['summary']}")
                st.markdown(f"[Read Full Article]({row['url']})")
    else:
        st.success("No high-risk articles found in current selection.")

    # Raw Data Section
    st.markdown("### 📄 Article Data")
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df[['title', 'date', 'risk_level', 'fraud_categories_str', 'sentiment', 'url']])

if __name__ == "__main__":
    main()
