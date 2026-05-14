import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol, period='1mo', interval='1h'):
        """Fetch stock data with caching"""
        cache_key = f"{symbol}_{period}_{interval}"
        
        # Check cache (5 minutes TTL)
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < 300:
                return data
        
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                return None
                
            # Cache result
            self.cache[cache_key] = (df, datetime.now())
            return df
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol):
        """Get real-time current price"""
        try:
            stock = yf.Ticker(symbol)
            return stock.info.get('regularMarketPrice', None)
        except:
            return None

    def get_ihsg_index(self):
        """Get IHSG index data"""
        return self.get_stock_data('^JKSE', period='1mo', interval='1h')
