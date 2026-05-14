import streamlit as st
from idx_scraper import IDXScraper

# Initialize scraper
@st.cache_data(ttl=86400)  # Cache selama 24 jam
def get_all_stocks():
    """Auto-fetch semua saham dari IDX dengan caching"""
    scraper = IDXScraper()
    stocks = scraper.get_all_stocks()
    
    # Pastikan minimal ada 100+ saham
    if len(stocks) < 100:
        # Fallback ke static list
        stocks = scraper.get_static_stocks()
    
    return stocks

# Auto-fetch stocks dari IDX
IHSG_STOCKS = get_all_stocks()

# Timeframes
TIMEFRAMES = {
    '5 Menit': '5m',
    '15 Menit': '15m', 
    '30 Menit': '30m',
    '1 Jam': '1h',
    '4 Jam': '4h',
    '1 Hari': '1d',
    '1 Minggu': '1wk'
}

# Scoring weights
SCORING_WEIGHTS = {
    'trend': 0.35,
    'momentum': 0.30,
    'volume': 0.20,
    'volatility': 0.15
}

# Untuk debug - lihat berapa saham yang berhasil di-load
print(f"✅ Loaded {len(IHSG_STOCKS)} stocks from IDX")
