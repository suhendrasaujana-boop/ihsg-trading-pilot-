import pandas as pd
import numpy as np

class TechnicalIndicators:
    
    @staticmethod
    def add_ema(df, period=20):
        """Add Exponential Moving Average"""
        df[f'ema_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
        return df
    
    @staticmethod
    def add_macd(df):
        """Add MACD indicator"""
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_diff'] = df['macd'] - df['macd_signal']
        return df
    
    @staticmethod
    def add_rsi(df, period=14):
        """Add RSI indicator"""
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def add_bollinger_bands(df, period=20):
        """Add Bollinger Bands"""
        df['bb_middle'] = df['Close'].rolling(window=period).mean()
        std = df['Close'].rolling(window=period).std()
        df['bb_upper'] = df['bb_middle'] + (std * 2)
        df['bb_lower'] = df['bb_middle'] - (std * 2)
        return df
    
    @staticmethod
    def add_volume_indicators(df):
        """Add volume indicators"""
        df['volume_ma'] = df['Volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_ma']
        return df
    
    @staticmethod
    def add_supertrend(df, period=10, multiplier=3):
        """Add Supertrend indicator - simple version"""
        # Initialize columns
        df['atr'] = 0.0
        df['supertrend'] = 0.0
        df['supertrend_direction'] = 1
        
        if len(df) < period + 1:
            return df
        
        try:
            high = df['High']
            low = df['Low']
            close = df['Close']
            
            # Calculate ATR
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            df['atr'] = atr
            
            # Calculate bands
            hl_avg = (high + low) / 2
            upper_band = hl_avg + (multiplier * atr)
            lower_band = hl_avg - (multiplier * atr)
            
            # Determine direction
            direction = 1
            for i in range(1, len(df)):
                if close.iloc[i] > upper_band.iloc[i-1]:
                    direction = 1
                elif close.iloc[i] < lower_band.iloc[i-1]:
                    direction = -1
                else:
                    direction = direction
                
                df.loc[df.index[i], 'supertrend_direction'] = direction
                
                if direction == 1:
                    df.loc[df.index[i], 'supertrend'] = lower_band.iloc[i]
                else:
                    df.loc[df.index[i], 'supertrend'] = upper_band.iloc[i]
                    
        except Exception as e:
            print(f"Supertrend calculation error: {e}")
        
        return df
    
    @staticmethod
    def calculate_all(df):
        """Calculate all indicators"""
        try:
            df = TechnicalIndicators.add_ema(df, 20)
            df = TechnicalIndicators.add_ema(df, 50)
            df = TechnicalIndicators.add_macd(df)
            df = TechnicalIndicators.add_rsi(df)
            df = TechnicalIndicators.add_bollinger_bands(df)
            df = TechnicalIndicators.add_volume_indicators(df)
            df = TechnicalIndicators.add_supertrend(df)
        except Exception as e:
            print(f"Error in calculate_all: {e}")
        
        return df
