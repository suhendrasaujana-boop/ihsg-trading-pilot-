import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz # Tambahkan ini untuk timezone

class DataFetcher:
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol, period='1mo', interval='1h'):
        """Fetch stock data with caching"""
        cache_key = f"{symbol}_{period}_{interval}"
        
        # Check cache (5 minutes TTL)
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).total_seconds() < 300:
                return data
        
        try:
            stock = yf.Ticker(symbol)
            # Tambahkan auto_adjust=False agar data konsisten
            df = stock.history(period=period, interval=interval, auto_adjust=False)
            
            if df.empty:
                return None
            
            # FIX: Konversi Timezone ke WIB (Asia/Jakarta)
            if df.index.tz is not None:
                df.index = df.index.tz_convert('Asia/Jakarta')
            else:
                # Jika tidak ada timezone (UTC), localize dulu baru convert
                df.index = df.index.tz_localize('UTC').tz_convert('Asia/Jakarta')
                
            # Opsional: Hapus baris yang harganya 0 atau NaN
            df = df[df['Close'] > 0]
                
            # Cache result
            self.cache[cache_key] = (df, datetime.now())
            return df
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol):
        """Get real-time current price (data paling fresh)"""
        try:
            stock = yf.Ticker(symbol)
            # fast_info lebih cepat dan lebih real-time daripada info
            return stock.fast_info.get('last_price', None)
        except Exception:
            return None

    def get_ihsg_index(self):
        """Get IHSG index data"""
        return self.get_stock_data('^JKSE', period='1mo', interval='1h')
