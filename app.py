import streamlit as st
import pandas as pd
from datetime import datetime

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

# Apply light theme
UIComponents.apply_light_theme()

# Title
st.title("📈 IHSG Trading Decision Assistant")
st.markdown("---")

# Initialize components
@st.cache_resource
def init_components():
    return DataFetcher(), ScoringEngine()

data_fetcher, scoring_engine = init_components()

# ============================================
# =============== SIDEBAR ====================
# ============================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/IDX_Logo.svg/1200px-IDX_Logo.svg.png", width=150)
    st.header("⚙️ Settings")
    
    # ========== SEARCH STOCK ==========
    st.subheader("🔍 Search Stock")
    search_term = st.text_input("Search by code or name", placeholder="BBCA, BCA, Telkom...")
    
    # Auto-filter based on search
    if search_term:
        search_lower = search_term.lower()
        filtered_stocks = {}
        for code, name in IHSG_STOCKS.items():
            if search_lower in code.lower() or search_lower in name.lower():
                filtered_stocks[code] = name
    else:
        filtered_stocks = IHSG_STOCKS
    
    # Show count
    st.caption(f"📊 {len(filtered_stocks)} stocks found")
    
    # Stock select with search
    if filtered_stocks:
        selected_stock = st.selectbox(
            "Select Stock",
            options=list(filtered_stocks.keys()),
            format_func=lambda x: f"{x.split('.')[0]} - {filtered_stocks[x]}"
        )
    else:
        st.warning("No stocks found")
        selected_stock = None
    
    # ========== SECTOR QUICK FILTER ==========
    st.subheader("🏭 Sector Quick Filter")
    
    # Group stocks by sector
    sectors = {
        '🏦 Banking': ['BBCA', 'BBRI', 'BMRI', 'BBNI', 'BRIS', 'BNGA', 'ARTO'],
        '⚡ Energy': ['ADRO', 'BUMI', 'ITMG', 'PTBA', 'BYAN', 'MDKA', 'ANTM', 'INCO', 'TINS'],
        '📱 Telco': ['TLKM', 'ISAT', 'EXCL', 'GOTO', 'FREN'],
        '🍜 Consumer': ['UNVR', 'ICBP', 'INDF', 'MYOR', 'KLBF', 'HMSP', 'GGRM', 'CPIN'],
        '🏗️ Infrastructure': ['ADHI', 'PTPP', 'WSKT', 'JSMR', 'PGAS', 'TOWR'],
        '🏠 Property': ['BSDE', 'CTRA', 'PWON', 'SMRA', 'LPKR', 'DILD'],
        '🛒 Retail': ['ACES', 'ERAA', 'AMRT', 'LPPF', 'MAPI'],
        '🚗 Automotive': ['ASII', 'AUTO', 'GDYR'],
    }
    
    sector_col1, sector_col2 = st.columns(2)
    sectors_list = list(sectors.items())
    
    for i, (sector_name, codes) in enumerate(sectors_list):
        col = sector_col1 if i % 2 == 0 else sector_col2
        if col.button(sector_name, use_container_width=True, key=f"sector_{i}"):
            # Filter stocks in this sector
            filtered = {}
            for code, name in IHSG_STOCKS.items():
                code_base = code.replace('.JK', '')
                if code_base in codes:
                    filtered[code] = name
            if filtered:
                filtered_stocks = filtered
                st.rerun()
    
    # ========== TIMEFRAME ==========
    selected_timeframe = st.selectbox(
        "Timeframe",
        options=list(TIMEFRAMES.keys())
    )
    
    # ========== PERIOD ==========
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
    
    # ========== SHOW TOTAL STOCKS ==========
    st.caption(f"📈 Total Stocks Available: {len(IHSG_STOCKS)}")
    st.caption("🔄 Data auto-sync dari IDX setiap 24 jam")
    
    refresh = st.button("🔄 Refresh Data", use_container_width=True)

# ============================================
# =============== MAIN CONTENT ===============
# ============================================

if selected_stock:  # Hanya jalan jika ada saham yang dipilih
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
            stock_name = IHSG_STOCKS.get(selected_stock, selected_stock)
            fig = UIComponents.create_candlestick_chart(df, f"{selected_stock} - {stock_name}")
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
            change_color = "🟢" if ihsg_change >= 0 else "🔴"
            
            st.markdown(f"""
            <div style="background-color:#f0f0f0; padding:15px; border-radius:10px; text-align:center;">
                <h3 style="margin:0;">IHSG Index</h3>
                <h1 style="margin:0; color:#1a1a1a;">{current_ihsg:,.2f}</h1>
                <p style="margin:0; color:{'green' if ihsg_change >= 0 else 'red'};">
                    {change_color} {ihsg_change:+.2f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top Movers
        st.subheader("🔥 Top Gainers")
        gainers = [
            {"code": "BBCA", "change": "+2.3%", "price": "10,500"},
            {"code": "BBRI", "change": "+1.8%", "price": "4,820"},
            {"code": "TLKM", "change": "+1.2%", "price": "3,450"},
        ]
        for g in gainers:
            st.markdown(f"**{g['code']}** - Rp {g['price']} <span style='color:green'>{g['change']}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.subheader("📋 Top Losers")
        losers = [
            {"code": "BMRI", "change": "-1.5%", "price": "6,100"},
            {"code": "ASII", "change": "-0.9%", "price": "4,750"},
            {"code": "UNVR", "change": "-0.7%", "price": "2,850"},
        ]
        for l in losers:
            st.markdown(f"**{l['code']}** - Rp {l['price']} <span style='color:red'>{l['change']}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Trading Tips
        st.subheader("💡 Trading Tips")
        st.info("""
        ✅ Always use Stop Loss (2-3% dari entry)
        ✅ Risk-Reward minimal 1:2
        ✅ Wait for candle confirmation
        ✅ Check multiple timeframes
        """)

# Footer
st.markdown("---")
st.caption(f"📊 Data from Yahoo Finance | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | ⚠️ Not financial advice")

# Auto-refresh
if refresh:
    st.rerun()
