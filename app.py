import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from config import IHSG_STOCKS, TIMEFRAMES
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from scoring import ScoringEngine
from ui_components import UIComponents

# Page config
st.set_page_config(
    page_title="IHSG Trading Decision App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .css-1d391kg {
        background-color: #1a1c23;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📈 IHSG Trading Decision Assistant")
st.markdown("---")

# Initialize components
@st.cache_resource
def init_components():
    return DataFetcher(), ScoringEngine()

data_fetcher, scoring_engine = init_components()

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/IDX_Logo.svg/1200px-IDX_Logo.svg.png", width=150)
    st.header("⚙️ Settings")
    
    # Stock selection
    selected_stock = st.selectbox(
        "Select Stock",
        options=list(IHSG_STOCKS.keys()),
        format_func=lambda x: f"{x.split('.')[0]} - {IHSG_STOCKS[x]}"
    )
    
    # Timeframe selection
    selected_timeframe = st.selectbox(
        "Timeframe",
        options=list(TIMEFRAMES.keys()),
        format_func=lambda x: f"{x} - {TIMEFRAMES[x]}"
    )
    
    # Period
    period = st.selectbox(
        "Data Period",
        options=['1d', '5d', '1mo', '3mo', '6mo', '1y'],
        index=2
    )
    
    st.markdown("---")
    st.info("""
    **How it works:**
    1. Multi-indicator scoring
    2. Weighted signal generation
    3. Real-time analysis
    """)
    
    refresh = st.button("🔄 Refresh Data", use_container_width=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Technical Analysis")
    
    # Fetch data
    interval = TIMEFRAMES[selected_timeframe]
    df = data_fetcher.get_stock_data(selected_stock, period=period, interval=interval)
    
    if df is not None and not df.empty:
        # Calculate indicators
        df = TechnicalIndicators.calculate_all(df)
        
        # Calculate scores
        signal_result = scoring_engine.calculate_total_score(df)
        
        # Display signal
        current_price = df['Close'].iloc[-1]
        UIComponents.display_signal_card(signal_result, current_price)
        
        # Display metrics
        UIComponents.display_metrics(df)
        
        # Display chart
        fig = UIComponents.create_candlestick_chart(df, f"{selected_stock} - {IHSG_STOCKS[selected_stock]}")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display recent data
        with st.expander("📋 Recent Data"):
            recent_data = df[['Open', 'High', 'Low', 'Close', 'Volume', 'rsi', 'macd_diff']].tail(10)
            recent_data.index = recent_data.index.strftime('%Y-%m-%d %H:%M')
            st.dataframe(recent_data, use_container_width=True)
        
    else:
        st.error("Failed to fetch data. Please try again.")

with col2:
    st.subheader("📈 Market Overview")
    
    # IHSG Index
    ihsg_df = data_fetcher.get_ihsg_index()
    if ihsg_df is not None and not ihsg_df.empty:
        current_ihsg = ihsg_df['Close'].iloc[-1]
        ihsg_change = ((ihsg_df['Close'].iloc[-1] - ihsg_df['Close'].iloc[-2]) / ihsg_df['Close'].iloc[-2]) * 100
        
        st.metric("IHSG Index", f"{current_ihsg:,.2f}", f"{ihsg_change:.2f}%")
    
    st.markdown("---")
    
    # Watchlist
    st.subheader("📋 Quick Watchlist")
    watchlist = ['BBCA.JK', 'BBRI.JK', 'TLKM.JK']
    
    for symbol in watchlist:
        price = data_fetcher.get_current_price(symbol)
        if price:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{symbol.split('.')[0]}**")
            with col_b:
                st.write(f"Rp {price:,.0f}")
    
    st.markdown("---")
    
    # Trading Tips
    st.subheader("💡 Trading Tips")
    st.info("""
    ✅ Always use Stop Loss
    ✅ Risk-Reward min 1:2
    ✅ Wait for confirmation
    ✅ Check multiple timeframes
    """)

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data from Yahoo Finance")

# Auto-refresh
if refresh:
    st.rerun()
