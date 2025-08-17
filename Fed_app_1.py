# Ron Paul Federal Reserve Analysis Dashboard
# A dedication to Dr. Ron Paul's tireless work exposing the Federal Reserve system

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Fed Analysis Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Ron Paul theme with improved visibility
st.markdown("""
<style>
    /* Main theme colors and text visibility */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Dedication box styling */
    .dedication {
        font-size: 1.2rem;
        color: #8b0000;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #f0f8ff;
        border-left: 5px solid #1f4e79;
        border-radius: 5px;
    }
    
    /* Metric cards styling */
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        color: #000000;
    }
    
    /* Warning/info boxes styling */
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
        font-weight: 500;
    }
    
    /* Ensure all text is visible */
    .stMarkdown, .stText, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Sidebar styling - multiple selectors for different Streamlit versions */
    .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    
    /* Sidebar content styling */
    .css-1d391kg *, .css-1lcbmhc *, .css-17eq0hr *, [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    /* Sidebar text elements */
    .css-1d391kg .stMarkdown, .css-1d391kg p, .css-1d391kg div, .css-1d391kg span,
    .css-1lcbmhc .stMarkdown, .css-1lcbmhc p, .css-1lcbmhc div, .css-1lcbmhc span,
    .css-17eq0hr .stMarkdown, .css-17eq0hr p, .css-17eq0hr div, .css-17eq0hr span,
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
        color: #000000 !important;
        background-color: transparent !important;
    }
    
    /* Sidebar headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4, .css-1d391kg h5, .css-1d391kg h6,
    .css-1lcbmhc h1, .css-1lcbmhc h2, .css-1lcbmhc h3, .css-1lcbmhc h4, .css-1lcbmhc h5, .css-1lcbmhc h6,
    .css-17eq0hr h1, .css-17eq0hr h2, .css-17eq0hr h3, .css-17eq0hr h4, .css-17eq0hr h5, .css-17eq0hr h6,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6 {
        color: #1f4e79 !important;
        font-weight: bold !important;
    }
    
    /* Sidebar selectbox styling */
    .css-1d391kg .stSelectbox, .css-1lcbmhc .stSelectbox, .css-17eq0hr .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox {
        color: #000000 !important;
    }
    
    /* Sidebar selectbox labels */
    .css-1d391kg .stSelectbox label, .css-1lcbmhc .stSelectbox label, .css-17eq0hr .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar selectbox dropdown */
    .css-1d391kg .stSelectbox > div, .css-1lcbmhc .stSelectbox > div, .css-17eq0hr .stSelectbox > div,
    [data-testid="stSidebar"] .stSelectbox > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    /* Aggressive selectbox fix - target all possible elements */
    div[data-baseweb="select"],
    div[data-baseweb="select"] *,
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    .stSelectbox,
    .stSelectbox *,
    [data-testid="stSidebar"] div[data-baseweb="select"],
    [data-testid="stSidebar"] div[data-baseweb="select"] *,
    [data-testid="stSidebar"] div[data-baseweb="popover"],
    [data-testid="stSidebar"] div[data-baseweb="popover"] *,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox * {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #dee2e6 !important;
    }
    
    /* Target the specific dropdown menu that appears */
    div[data-baseweb="popover"] div[role="listbox"],
    div[data-baseweb="popover"] div[role="listbox"] *,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] ul *,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] li * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Override any dark theme classes */
    .css-1d391kg div[data-baseweb="select"],
    .css-1d391kg div[data-baseweb="select"] *,
    .css-1d391kg div[data-baseweb="popover"],
    .css-1d391kg div[data-baseweb="popover"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Nuclear option - override everything with selectbox class */
    [class*="selectbox"] *,
    [class*="Select"] *,
    [class*="dropdown"] *,
    [class*="menu"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Metric value styling */
    .css-1xarl3l {
        color: #000000 !important;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        color: #1f4e79 !important;
        font-weight: bold;
    }
    
    /* Subheaders with icons */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1f4e79 !important;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460 !important;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724 !important;
    }
    
    /* Error boxes */
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24 !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        color: #000000 !important;
    }
    
    /* Table headers */
    .dataframe th {
        background-color: #1f4e79 !important;
        color: #ffffff !important;
        font-weight: bold;
    }
    
    /* Table cells */
    .dataframe td {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Plotly chart backgrounds */
    .js-plotly-plot {
        background-color: #ffffff !important;
    }
    
    /* Ensure bullet points and lists are visible */
    ul, ol, li {
        color: #000000 !important;
    }
    
    /* Strong/bold text */
    strong, b {
        color: #1f4e79 !important;
        font-weight: bold;
    }
    
    /* Italic text */
    em, i {
        color: #8b0000 !important;
    }
    
    /* Code blocks */
    code {
        background-color: #f8f9fa;
        color: #e83e8c;
        padding: 2px 4px;
        border-radius: 3px;
    }
    
    /* Links */
    a {
        color: #1f4e79 !important;
        text-decoration: underline;
    }
    
    /* Blockquotes */
    blockquote {
        border-left: 4px solid #1f4e79;
        padding-left: 1rem;
        margin-left: 0;
        color: #8b0000 !important;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header and dedication
st.markdown('<h1 class="main-header">🏛️ The Federal Reserve Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown('''
<div class="dedication">
"This dashboard presents a detailed analysis of inflation, government spending, and monetary manipulation."
<br><br>
</div>
''', unsafe_allow_html=True)

# Sidebar for navigation and controls
st.sidebar.title("📊 Analysis Controls")
st.sidebar.markdown("---")

# Data fetching functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_fred_data(series_id, api_key, start_date=None, end_date=None):
    """Fetch data from FRED API with optional date filtering"""
    endpoint = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json'
    }
    
    if start_date:
        params['observation_start'] = start_date
    if end_date:
        params['observation_end'] = end_date
    
    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        df = pd.DataFrame(data['observations'])
        df = df[df['value'] != '.'].copy()
        df['value'] = pd.to_numeric(df['value'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={'value': series_id})
        return df[['date', series_id]]
    except Exception as e:
        st.error(f"Error fetching {series_id}: {str(e)}")
        return pd.DataFrame()

def get_date_range(time_period):
    """Get start and end dates based on time period selection"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    if time_period == "Since Nixon Shock (1971)":
        start_date = "1971-08-15"
    elif time_period == "Since Fed Creation (1913)":
        start_date = "1913-12-23"
    elif time_period == "Last 50 Years":
        start_date = (datetime.now() - timedelta(days=50*365)).strftime('%Y-%m-%d')
    elif time_period == "Last 20 Years":
        start_date = (datetime.now() - timedelta(days=20*365)).strftime('%Y-%m-%d')
    else:  # Custom Range - for now default to Nixon Shock
        start_date = "1971-08-15"
    
    return start_date, end_date

# Get API key
api_key = os.getenv('FED_API_KEY')
if not api_key:
    st.error("⚠️ FRED API key not found. Please set FED_API_KEY in your .env file.")
    st.stop()

# Sidebar controls
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Complete Analysis", "Fiscal Policy Deep Dive", "Monetary Policy Exposure", 
     "Dollar Debasement Tracker", "Bretton Woods Era (1913-1971)", 
     "Fiat Currency Era (Post-1971)", "Two Eras Comparison: Dollar Value & Economic Impact"]
)

time_period = st.sidebar.selectbox(
    "Time Period",
    ["Last 50 Years", "Last 20 Years"]
)

# Define FRED series based on the guide
FRED_SERIES = {
    # Fiscal Policy
    'FGEXPND': 'Federal Government Expenditures',
    'FYFSD': 'Federal Surplus/Deficit',
    'FYGFDPUN': 'Federal Debt Held by Public',
    'A091RC1Q027SBEA': 'Interest Payments on Federal Debt',
    
    # Monetary Policy
    'M1SL': 'M1 Money Stock',
    'M2SL': 'M2 Money Stock',
    'BASE': 'Monetary Base',
    'CPIAUCSL': 'Consumer Price Index',
    'CPILFESL': 'Core CPI',
    'PCEPI': 'PCE Price Index',
    'FEDFUNDS': 'Federal Funds Rate',
    
    # Treasury & Interest Rates
    'DGS10': '10-Year Treasury Yield',
    'T5YIE': '5-Year Breakeven Inflation',
    
    # Dollar & Trade
    'DTWEXBGS': 'Broad Dollar Index',
    'NETEXP': 'Net Exports',
    
    # Economic Indicators
    'GDP': 'Gross Domestic Product',
    'UNRATE': 'Unemployment Rate',
    'MEHOINUSA672N': 'Real Median Household Income'
}

# Main analysis section
if analysis_type == "Complete Analysis":
    st.header("🎯 The Complete Analysis: Exposing the Fed's Impact")
    
    # Get date range based on time period selection
    start_date, end_date = get_date_range(time_period)
    
    # Display selected time period
    st.info(f"📅 Analyzing data from {start_date} to {end_date}")
    
    # Fetch key data
    with st.spinner("Fetching Federal Reserve data..."):
        # Core datasets for Ron Paul analysis
        key_series = ['M2SL', 'CPIAUCSL', 'FGEXPND', 'DGS10', 'FEDFUNDS', 'GDP']
        data_dict = {}
        
        for series in key_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                data_dict[series] = df
    
    if data_dict:
        # Create the main dashboard
        col1, col2, col3 = st.columns(3)
        
        # Calculate recent metrics
        latest_m2 = data_dict['M2SL'][data_dict['M2SL']['M2SL'].notna()].iloc[-1]['M2SL'] if 'M2SL' in data_dict else 0
        latest_cpi = data_dict['CPIAUCSL'][data_dict['CPIAUCSL']['CPIAUCSL'].notna()].iloc[-1]['CPIAUCSL'] if 'CPIAUCSL' in data_dict else 0
        latest_spending = data_dict['FGEXPND'][data_dict['FGEXPND']['FGEXPND'].notna()].iloc[-1]['FGEXPND'] if 'FGEXPND' in data_dict else 0
        
        with col1:
            st.metric(
                "💰 M2 Money Supply",
                f"${latest_m2:,.0f}B",
                help="The Fed's money printing machine in action"
            )
        
        with col2:
            st.metric(
                "📈 Consumer Price Index",
                f"{latest_cpi:.1f}",
                help="The hidden tax of inflation on American families"
            )
        
        with col3:
            st.metric(
                "🏛️ Federal Spending",
                f"${latest_spending:,.0f}B",
                help="Government spending fueling the debt crisis"
            )
        
        # The Ron Paul Chart: Money Supply vs Inflation vs Government Spending
        st.subheader("📊 Money Printing, Inflation, and Government Spending")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Money Supply Growth (M2)', 'Inflation Erosion (CPI)', 
                          'Government Spending Explosion', 'The Fed Funds Rate Manipulation'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Money Supply
        if 'M2SL' in data_dict:
            m2_data = data_dict['M2SL']
            fig.add_trace(
                go.Scatter(x=m2_data['date'], y=m2_data['M2SL'], 
                          name='M2 Money Supply', line=dict(color='red', width=3)),
                row=1, col=1
            )
        
        # Inflation
        if 'CPIAUCSL' in data_dict:
            cpi_data = data_dict['CPIAUCSL']
            fig.add_trace(
                go.Scatter(x=cpi_data['date'], y=cpi_data['CPIAUCSL'], 
                          name='Consumer Price Index', line=dict(color='orange', width=3)),
                row=1, col=2
            )
        
        # Government Spending
        if 'FGEXPND' in data_dict:
            spending_data = data_dict['FGEXPND']
            fig.add_trace(
                go.Scatter(x=spending_data['date'], y=spending_data['FGEXPND'], 
                          name='Federal Spending', line=dict(color='blue', width=3)),
                row=2, col=1
            )
        
        # Fed Funds Rate
        if 'FEDFUNDS' in data_dict:
            fed_data = data_dict['FEDFUNDS']
            fig.add_trace(
                go.Scatter(x=fed_data['date'], y=fed_data['FEDFUNDS'], 
                          name='Fed Funds Rate', line=dict(color='green', width=3)),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="Ron Paul's Warnings Visualized: The Fed's Economic Manipulation")
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation Analysis
        st.subheader("🔗 The Dangerous Correlations Ron Paul Warned About")
        
        # Calculate correlations between key metrics
        if len(data_dict) >= 3:
            # Merge data for correlation analysis
            merged_data = None
            for series, df in data_dict.items():
                if merged_data is None:
                    merged_data = df.set_index('date')
                else:
                    merged_data = merged_data.join(df.set_index('date'), how='outer')
            
            if merged_data is not None:
                # Calculate correlation matrix
                corr_matrix = merged_data.corr()
                
                # Create correlation heatmap
                fig_corr = px.imshow(corr_matrix, 
                                   title="Correlation Matrix: How Fed Policies Connect",
                                   color_continuous_scale='RdBu_r',
                                   aspect='auto')
                st.plotly_chart(fig_corr, use_container_width=True)
                

elif analysis_type == "Fiscal Policy Deep Dive":
    st.header("💸 Fiscal Policy Deep Dive: The Spending Addiction")
    
    # Get date range based on time period selection
    start_date, end_date = get_date_range(time_period)
    st.info(f"📅 Analyzing fiscal data from {start_date} to {end_date}")
    
    # Fetch fiscal data
    fiscal_series = ['FGEXPND', 'FYFSD', 'FYGFDPUN', 'GDP']
    fiscal_data = {}
    
    with st.spinner("Loading fiscal policy data..."):
        for series in fiscal_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                fiscal_data[series] = df
    
    if fiscal_data:
        # Debt-to-GDP ratio calculation
        if 'FYGFDPUN' in fiscal_data and 'GDP' in fiscal_data:
            debt_data = fiscal_data['FYGFDPUN'].set_index('date')
            gdp_data = fiscal_data['GDP'].set_index('date')
            
            # Merge and calculate ratio
            combined = debt_data.join(gdp_data, how='inner')
            combined['debt_to_gdp'] = (combined['FYGFDPUN'] / combined['GDP']) * 100
            
            # Plot debt-to-GDP trend
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=combined.index, 
                y=combined['debt_to_gdp'],
                mode='lines',
                name='Debt-to-GDP Ratio',
                line=dict(color='red', width=3)
            ))
            
            fig.update_layout(
                title="🚨 Federal Debt-to-GDP Ratio: The Unsustainable Path",
                xaxis_title="Year",
                yaxis_title="Debt-to-GDP Ratio (%)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Current debt level warning
            current_ratio = combined['debt_to_gdp'].iloc[-1]
            st.markdown(f"""
            <div class="warning-box">
            <strong>🚨 Current Federal Debt-to-GDP Ratio: {current_ratio:.1f}%</strong><br>
            </div>
            """, unsafe_allow_html=True)

elif analysis_type == "Monetary Policy Exposure":
    st.header("🖨️ Monetary Policy Exposure: The Money Printing Machine")
    
    # Get date range based on time period selection
    start_date, end_date = get_date_range(time_period)
    st.info(f"📅 Analyzing monetary data from {start_date} to {end_date}")
    
    # Fetch monetary data
    monetary_series = ['M1SL', 'M2SL', 'BASE', 'CPIAUCSL', 'FEDFUNDS']
    monetary_data = {}
    
    with st.spinner("Exposing the Fed's monetary manipulation..."):
        for series in monetary_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                monetary_data[series] = df
    
    if monetary_data:
        # Money supply growth chart
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Money Supply Explosion', 'The Inflation Consequence'),
            vertical_spacing=0.1
        )
        
        # M1 and M2 money supply
        if 'M1SL' in monetary_data:
            m1_data = monetary_data['M1SL']
            fig.add_trace(
                go.Scatter(x=m1_data['date'], y=m1_data['M1SL'], 
                          name='M1 Money Supply', line=dict(color='blue')),
                row=1, col=1
            )
        
        if 'M2SL' in monetary_data:
            m2_data = monetary_data['M2SL']
            fig.add_trace(
                go.Scatter(x=m2_data['date'], y=m2_data['M2SL'], 
                          name='M2 Money Supply', line=dict(color='red')),
                row=1, col=1
            )
        
        # Inflation
        if 'CPIAUCSL' in monetary_data:
            cpi_data = monetary_data['CPIAUCSL']
            fig.add_trace(
                go.Scatter(x=cpi_data['date'], y=cpi_data['CPIAUCSL'], 
                          name='Consumer Price Index', line=dict(color='orange')),
                row=2, col=1
            )
        
        fig.update_layout(height=800, title_text="The Fed's Money Printing and Its Inflationary Consequences")
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate money supply growth rates
        if 'M2SL' in monetary_data:
            m2_data = monetary_data['M2SL'].set_index('date')
            m2_data['M2_growth'] = m2_data['M2SL'].pct_change(periods=12) * 100  # Year-over-year growth
            
            recent_growth = m2_data['M2_growth'].dropna().iloc[-1]

elif analysis_type == "Dollar Debasement Tracker":
    st.header("💵 Dollar Debasement Tracker: The Purchasing Power Destruction")
    
    # For dollar debasement, always show the full historical picture from 1913 to present
    start_date = "1913-12-23"  # Fed creation date
    end_date = datetime.now().strftime('%Y-%m-%d')
    st.info(f"📅 Analyzing holistic dollar debasement from {start_date} to {end_date}")
    
    # Fetch dollar-related data
    dollar_series = ['CPIAUCSL', 'DTWEXBGS', 'DGS10']
    dollar_data = {}
    
    with st.spinner("Tracking dollar debasement..."):
        for series in dollar_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                dollar_data[series] = df
    
    if 'CPIAUCSL' in dollar_data:
        cpi_data = dollar_data['CPIAUCSL'].set_index('date')
        
        # Calculate purchasing power relative to the first data point available
        first_cpi = cpi_data['CPIAUCSL'].iloc[0]
        cpi_data['purchasing_power'] = first_cpi / cpi_data['CPIAUCSL']
        
        # Purchasing power chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=cpi_data.index,
            y=cpi_data['purchasing_power'],
            mode='lines',
            name='Dollar Purchasing Power',
            line=dict(color='red', width=3),
            fill='tonexty'
        ))
        
        first_date = cpi_data.index[0].strftime('%Y')
        fig.update_layout(
            title=f"💀 Dollar Purchasing Power Decline Since {first_date}",
            xaxis_title="Year",
            yaxis_title=f"Purchasing Power ({first_date} = 1.00)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Current purchasing power
        current_power = cpi_data['purchasing_power'].iloc[-1]
        destruction_pct = (1 - current_power) * 100
        
        st.markdown(f"""
        <div class="warning-box">
        <strong>💀 Dollar Purchasing Power Lost Since {first_date}: {destruction_pct:.1f}%</strong><br>
        What cost $1.00 in {first_date} now costs ${1/current_power:.2f}. This demonstrates the hidden tax of inflation.
        </div>
        """, unsafe_allow_html=True)

elif analysis_type == "Bretton Woods Era (1913-1971)":
    st.header("🏦 Bretton Woods Era: The Managed Gold System (1913-1971)")
    
    # Get date range based on time period selection
    start_date, end_date = get_date_range(time_period)
    
    st.info(f"📅 Analyzing Bretton Woods Era data from {start_date} to {end_date}")
    
    # Fetch key economic data for this period
    bretton_woods_series = ['CPIAUCSL', 'FGEXPND', 'GDP', 'UNRATE']
    bretton_woods_data = {}
    
    with st.spinner("Loading Bretton Woods Era data..."):
        for series in bretton_woods_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                bretton_woods_data[series] = df
    
    if bretton_woods_data:
        # Create metrics for the Bretton Woods era
        col1, col2, col3 = st.columns(3)
        
        # Calculate average metrics for the period
        if 'CPIAUCSL' in bretton_woods_data:
            cpi_data = bretton_woods_data['CPIAUCSL']
            avg_inflation = cpi_data['CPIAUCSL'].pct_change(periods=12).mean() * 100
            
            with col1:
                st.metric(
                    "📊 Average Annual Inflation",
                    f"{avg_inflation:.1f}%",
                    help="Inflation during the Bretton Woods era"
                )
        
        if 'FGEXPND' in bretton_woods_data:
            spending_data = bretton_woods_data['FGEXPND']
            spending_growth = ((spending_data['FGEXPND'].iloc[-1] / spending_data['FGEXPND'].iloc[0]) ** (1/58) - 1) * 100
            
            with col2:
                st.metric(
                    "🏛️ Gov Spending Growth",
                    f"{spending_growth:.1f}%/year",
                    help="Average annual government spending growth"
                )
        
        if 'GDP' in bretton_woods_data:
            gdp_data = bretton_woods_data['GDP']
            gdp_growth = ((gdp_data['GDP'].iloc[-1] / gdp_data['GDP'].iloc[0]) ** (1/58) - 1) * 100
            
            with col3:
                st.metric(
                    "📈 GDP Growth",
                    f"{gdp_growth:.1f}%/year",
                    help="Average annual GDP growth during Bretton Woods era"
                )
        
        # Create comprehensive chart for Bretton Woods era
        st.subheader("📊 Bretton Woods Era: The Managed System (1913-1971)")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Consumer Price Index', 'Federal Government Spending', 
                           'Gross Domestic Product', 'Unemployment Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # CPI
        if 'CPIAUCSL' in bretton_woods_data:
            cpi_data = bretton_woods_data['CPIAUCSL']
            fig.add_trace(
                go.Scatter(x=cpi_data['date'], y=cpi_data['CPIAUCSL'], 
                          name='CPI', line=dict(color='red', width=2)),
                row=1, col=1
            )
        
        # Government Spending
        if 'FGEXPND' in bretton_woods_data:
            spending_data = bretton_woods_data['FGEXPND']
            fig.add_trace(
                go.Scatter(x=spending_data['date'], y=spending_data['FGEXPND'], 
                          name='Federal Spending', line=dict(color='blue', width=2)),
                row=1, col=2
            )
        
        # GDP
        if 'GDP' in bretton_woods_data:
            gdp_data = bretton_woods_data['GDP']
            fig.add_trace(
                go.Scatter(x=gdp_data['date'], y=gdp_data['GDP'], 
                          name='GDP', line=dict(color='green', width=2)),
                row=2, col=1
            )
        
        # Unemployment
        if 'UNRATE' in bretton_woods_data:
            unrate_data = bretton_woods_data['UNRATE']
            fig.add_trace(
                go.Scatter(x=unrate_data['date'], y=unrate_data['UNRATE'], 
                          name='Unemployment', line=dict(color='orange', width=2)),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="Bretton Woods Era: Economic Indicators (1913-1971)")
        st.plotly_chart(fig, use_container_width=True)
        

elif analysis_type == "Fiat Currency Era (Post-1971)":
    st.header("💸 Fiat Currency Era: The Great Debasement (Post-1971)")
    
    # Get date range based on time period selection
    start_date, end_date = get_date_range(time_period)
    
    st.info(f"📅 Analyzing Fiat Currency Era data from {start_date} to {end_date}")
    
    # Fetch comprehensive data for fiat era
    fiat_era_series = ['M2SL', 'CPIAUCSL', 'FGEXPND', 'GDP', 'FEDFUNDS', 'FYGFDPUN']
    fiat_era_data = {}
    
    with st.spinner("Loading Fiat Currency Era data..."):
        for series in fiat_era_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                fiat_era_data[series] = df
    
    if fiat_era_data:
        # Calculate dramatic changes since 1971
        col1, col2, col3, col4 = st.columns(4)
        
        # Money Supply Explosion
        if 'M2SL' in fiat_era_data:
            m2_data = fiat_era_data['M2SL']
            m2_increase = ((m2_data['M2SL'].iloc[-1] / m2_data['M2SL'].iloc[0]) - 1) * 100
            
            with col1:
                st.metric(
                    "💰 M2 Money Supply Increase",
                    f"{m2_increase:,.0f}%",
                    help="Total increase in money supply since Nixon Shock"
                )
        
        # Inflation Destruction
        if 'CPIAUCSL' in fiat_era_data:
            cpi_data = fiat_era_data['CPIAUCSL']
            purchasing_power_lost = (1 - (cpi_data['CPIAUCSL'].iloc[0] / cpi_data['CPIAUCSL'].iloc[-1])) * 100
            
            with col2:
                st.metric(
                    "💀 Purchasing Power Lost",
                    f"{purchasing_power_lost:.0f}%",
                    help="Dollar purchasing power destroyed since 1971"
                )
        
        # Government Spending Explosion
        if 'FGEXPND' in fiat_era_data:
            spending_data = fiat_era_data['FGEXPND']
            spending_increase = ((spending_data['FGEXPND'].iloc[-1] / spending_data['FGEXPND'].iloc[0]) - 1) * 100
            
            with col3:
                st.metric(
                    "🏛️ Federal Spending Increase",
                    f"{spending_increase:,.0f}%",
                    help="Total increase in federal spending since 1971"
                )
        
        # National Debt Explosion
        if 'FYGFDPUN' in fiat_era_data:
            debt_data = fiat_era_data['FYGFDPUN']
            debt_increase = ((debt_data['FYGFDPUN'].iloc[-1] / debt_data['FYGFDPUN'].iloc[0]) - 1) * 100
            
            with col4:
                st.metric(
                    "📊 National Debt Increase",
                    f"{debt_increase:,.0f}%",
                    help="Total increase in national debt since 1971"
                )
        
        # The Great Debasement Chart
        st.subheader("📊 The Great Debasement: Fiat Currency Consequences (1971-Present)")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Money Supply Explosion (M2)', 'Inflation Acceleration (CPI)', 
                           'Government Spending Explosion', 'Federal Debt Crisis'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Money Supply
        if 'M2SL' in fiat_era_data:
            m2_data = fiat_era_data['M2SL']
            fig.add_trace(
                go.Scatter(x=m2_data['date'], y=m2_data['M2SL'], 
                          name='M2 Money Supply', line=dict(color='red', width=3)),
                row=1, col=1
            )
        
        # Inflation
        if 'CPIAUCSL' in fiat_era_data:
            cpi_data = fiat_era_data['CPIAUCSL']
            fig.add_trace(
                go.Scatter(x=cpi_data['date'], y=cpi_data['CPIAUCSL'], 
                          name='Consumer Price Index', line=dict(color='orange', width=3)),
                row=1, col=2
            )
        
        # Government Spending
        if 'FGEXPND' in fiat_era_data:
            spending_data = fiat_era_data['FGEXPND']
            fig.add_trace(
                go.Scatter(x=spending_data['date'], y=spending_data['FGEXPND'], 
                          name='Federal Spending', line=dict(color='blue', width=3)),
                row=2, col=1
            )
        
        # Federal Debt
        if 'FYGFDPUN' in fiat_era_data:
            debt_data = fiat_era_data['FYGFDPUN']
            fig.add_trace(
                go.Scatter(x=debt_data['date'], y=debt_data['FYGFDPUN'], 
                          name='Federal Debt', line=dict(color='purple', width=3)),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="The Fiat Currency Disaster: Ron Paul's Predictions Realized")
        st.plotly_chart(fig, use_container_width=True)
        
        # Decade-by-decade breakdown
        st.subheader("📊 Decade-by-Decade Breakdown: The Accelerating Crisis")
        
        # Create decade analysis for fiat era
        decades = ['1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
        decade_ranges = [
            ('1971-01-01', '1979-12-31'),
            ('1980-01-01', '1989-12-31'),
            ('1990-01-01', '1999-12-31'),
            ('2000-01-01', '2009-12-31'),
            ('2010-01-01', '2019-12-31'),
            ('2020-01-01', '2024-12-31')
        ]
        
        decade_data = []
        
        for i, (start, end) in enumerate(decade_ranges):
            decade_info = {'decade': decades[i]}
            
            # Calculate average inflation for decade
            if 'CPIAUCSL' in fiat_era_data:
                cpi_decade = fiat_era_data['CPIAUCSL'][
                    (fiat_era_data['CPIAUCSL']['date'] >= start) & 
                    (fiat_era_data['CPIAUCSL']['date'] <= end)
                ]
                if len(cpi_decade) > 12:
                    decade_info['avg_inflation'] = cpi_decade['CPIAUCSL'].pct_change(periods=12).mean() * 100
                else:
                    decade_info['avg_inflation'] = 0
            
            decade_data.append(decade_info)
        
        # Display decade comparison
        decade_df = pd.DataFrame(decade_data)
        if not decade_df.empty and 'avg_inflation' in decade_df.columns:
            fig_decades = go.Figure()
            fig_decades.add_trace(go.Bar(
                x=decade_df['decade'],
                y=decade_df['avg_inflation'],
                marker_color=['red' if x > 5 else 'orange' if x > 3 else 'green' for x in decade_df['avg_inflation']],
                text=[f"{x:.1f}%" for x in decade_df['avg_inflation']],
                textposition='auto'
            ))
            
            fig_decades.update_layout(
                title="Average Annual Inflation by Decade (Fiat Era)",
                xaxis_title="Decade",
                yaxis_title="Average Annual Inflation (%)",
                height=400
            )
            
            st.plotly_chart(fig_decades, use_container_width=True)

elif analysis_type == "Two Eras Comparison: Dollar Value & Economic Impact":
    st.header("⚖️ Two Eras Comparison: Dollar Value & Economic Impact")
    
    # Define the two eras with their characteristics
    st.subheader("📊 The Two Monetary Eras: A Side-by-Side Analysis")
    
    # Create three columns for era comparison
    col1, col2, col3 = st.columns(3)
    
    # Fetch data for comparison analysis
    st.subheader("📈 Comparative Economic Data Analysis")
    
    st.info("📊 Note: FRED API data is only available from 1913 onwards. The comparison below focuses on the Gold Standard Era (1913-1971) vs Fiat Currency Era (1971-Present) using reliable FRED data.")
    
    # Get date range based on time period selection
    start_date, end_date = get_date_range(time_period)
    st.info(f"📅 Analyzing comparative data from {start_date} to {end_date}")
    
    with st.spinner("Loading comparative economic data..."):
        # Fetch data for the selected time period
        comparison_series = ['CPIAUCSL', 'FGEXPND', 'GDP', 'M2SL', 'FYGFDPUN']
        comparison_data = {}
        
        for series in comparison_series:
            df = fetch_fred_data(series, api_key, start_date, end_date)
            if not df.empty:
                comparison_data[series] = df
        
        # Also fetch historical data for era comparison context
        gold_era_data = {}
        fiat_era_data = {}
        
        # Gold Standard Era (1913-1971) for historical context
        gold_series = ['CPIAUCSL', 'FGEXPND', 'GDP']
        for series in gold_series:
            df = fetch_fred_data(series, api_key, "1913-12-23", "1971-08-15")
            if not df.empty:
                gold_era_data[series] = df
        
        # Fiat Currency Era (1971-Present) for historical context
        fiat_series = ['CPIAUCSL', 'FGEXPND', 'GDP', 'M2SL', 'FYGFDPUN']
        for series in fiat_series:
            df = fetch_fred_data(series, api_key, "1971-08-15", datetime.now().strftime('%Y-%m-%d'))
            if not df.empty:
                fiat_era_data[series] = df
    
    # Create comprehensive comparison metrics
    st.subheader("🎯 Key Economic Indicators Comparison")
    
    # Calculate metrics for each era using only available FRED data
    era_metrics = {}
    
    # Gold Standard Era
    if gold_era_data:
        gold_inflation = 0
        gold_gdp_growth = 0
        
        if 'CPIAUCSL' in gold_era_data:
            cpi_data = gold_era_data['CPIAUCSL']
            gold_inflation = cpi_data['CPIAUCSL'].pct_change(periods=12).mean() * 100
        
        if 'GDP' in gold_era_data and len(gold_era_data['GDP']) > 1:
            gdp_data = gold_era_data['GDP']
            years = len(gdp_data) / 12  # Approximate years
            gold_gdp_growth = ((gdp_data['GDP'].iloc[-1] / gdp_data['GDP'].iloc[0]) ** (1/years) - 1) * 100
        
        era_metrics['Gold Standard (1913-1971)'] = {
            'avg_inflation': gold_inflation,
            'avg_gdp_growth': gold_gdp_growth,
            'currency_backing': 'Partial Gold',
            'monetary_system': 'Central Banking'
        }
    
    # Fiat Currency Era
    if fiat_era_data:
        fiat_inflation = 0
        fiat_gdp_growth = 0
        purchasing_power_lost = 0
        
        if 'CPIAUCSL' in fiat_era_data:
            cpi_data = fiat_era_data['CPIAUCSL']
            fiat_inflation = cpi_data['CPIAUCSL'].pct_change(periods=12).mean() * 100
            purchasing_power_lost = (1 - (cpi_data['CPIAUCSL'].iloc[0] / cpi_data['CPIAUCSL'].iloc[-1])) * 100
        
        if 'GDP' in fiat_era_data and len(fiat_era_data['GDP']) > 1:
            gdp_data = fiat_era_data['GDP']
            years = len(gdp_data) / 12  # Approximate years
            fiat_gdp_growth = ((gdp_data['GDP'].iloc[-1] / gdp_data['GDP'].iloc[0]) ** (1/years) - 1) * 100
        
        era_metrics['Fiat Currency (1971-Present)'] = {
            'avg_inflation': fiat_inflation,
            'avg_gdp_growth': fiat_gdp_growth,
            'dollar_purchasing_power_change': -purchasing_power_lost,
            'currency_backing': 'None (Fiat)',
            'monetary_system': 'Central Bank Monopoly'
        }
    
    # Only create charts if we have data for both eras
    if len(era_metrics) >= 2:
        # Create visual comparison charts for available data
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Average Annual Inflation (%)', 'Average GDP Growth (%)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        eras = list(era_metrics.keys())
        colors = ['orange', 'red'] if len(eras) == 2 else ['green', 'orange', 'red']
        
        # Inflation comparison
        inflation_values = [era_metrics[era]['avg_inflation'] for era in eras]
        fig.add_trace(
            go.Bar(x=eras, y=inflation_values, name='Inflation', 
                   marker_color=colors, text=[f"{v:.1f}%" for v in inflation_values], textposition='auto'),
            row=1, col=1
        )
        
        # GDP Growth comparison
        gdp_values = [era_metrics[era]['avg_gdp_growth'] for era in eras]
        fig.add_trace(
            go.Bar(x=eras, y=gdp_values, name='GDP Growth', 
                   marker_color=colors, text=[f"{v:.1f}%" for v in gdp_values], textposition='auto'),
            row=1, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, 
                         title_text="Economic Comparison: Gold Standard vs Fiat Currency Eras (FRED Data)")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display comparison table
        comparison_df = pd.DataFrame(era_metrics).T
        st.dataframe(comparison_df, use_container_width=True)
    
    else:
        st.warning("⚠️ Insufficient data available for era comparison. Please ensure FRED API access is working properly.")
    
    # Dollar purchasing power chart using actual CPI data
    if 'CPIAUCSL' in fiat_era_data:
        st.subheader("💵 Dollar Purchasing Power Decline (Based on CPI Data)")
        
        cpi_data = fiat_era_data['CPIAUCSL'].set_index('date')
        first_cpi = cpi_data['CPIAUCSL'].iloc[0]
        cpi_data['purchasing_power'] = first_cpi / cpi_data['CPIAUCSL']
        
        fig_power = go.Figure()
        fig_power.add_trace(go.Scatter(
            x=cpi_data.index,
            y=cpi_data['purchasing_power'],
            mode='lines',
            name='Dollar Purchasing Power',
            line=dict(color='red', width=3),
            fill='tonexty'
        ))
        
        first_date = cpi_data.index[0].strftime('%Y')
        fig_power.update_layout(
            title=f"💀 Dollar Purchasing Power Decline Since {first_date} (Fiat Era)",
            xaxis_title="Year",
            yaxis_title=f"Purchasing Power ({first_date} = 1.00)",
            height=500
        )
        
        st.plotly_chart(fig_power, use_container_width=True)

# Footer with Ron Paul quotes and dedication
st.markdown("---")

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
**About This Dashboard**
An analysis of the Federal Reserve System
""")
