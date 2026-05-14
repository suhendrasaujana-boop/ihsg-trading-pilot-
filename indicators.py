import pandas as pd
import numpy as np
import ta

class TechnicalIndicators:
    
    @staticmethod
    def add_ema(df, period=20):
        df[f'ema_{period}'] = ta.trend.EMAIndicator(df['Close'], window=period).ema_indicator()
        return df
    
    @staticmethod
    def add_macd(df):
        macd = ta.trend.MACD(df['Close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        return df
    
    @staticmethod
    def add_rsi(df, period=14):
        df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=period).rsi()
        return df
    
    @staticmethod
    def add_bollinger_bands(df, period=20):
        bb = ta.volatility.BollingerBands(df['Close'], window=period)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        return df
    
    @staticmethod
    def add_volume_indicators(df):
        df['volume_ma'] = df['Volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_ma']
        return df
    
    @staticmethod
    def add_supertrend(df, period=10, multiplier=3):
        """Supertrend indicator"""
        high = df['High']
        low = df['Low']
        close = df['Close']
        
        atr = ta.volatility.AverageTrueRange(high, low, close, window=period)
        df['atr'] = atr.average_true_range()
        
        hl_avg = (high + low) / 2
        upper_band = hl_avg + (multiplier * df['atr'])
        lower_band = hl_avg - (multiplier * df['atr'])
        
        df['supertrend'] = 0
        df['supertrend_direction'] = 1  # 1=up, -1=down
        
        for i in range(1, len(df)):
            if close.iloc[i] > upper_band.iloc[i-1]:
                df.loc[df.index[i], 'supertrend_direction'] = 1
            elif close.iloc[i] < lower_band.iloc[i-1]:
                df.loc[df.index[i], 'supertrend_direction'] = -1
            else:
                df.loc[df.index[i], 'supertrend_direction'] = df['supertrend_direction'].iloc[i-1]
            
            if df['supertrend_direction'].iloc[i] == 1:
                df.loc[df.index[i], 'supertrend'] = lower_band.iloc[i]
            else:
                df.loc[df.index[i], 'supertrend'] = upper_band.iloc[i]
        
        return df
    
    @staticmethod
    def calculate_all(df):
        """Calculate all indicators at once"""
        df = TechnicalIndicators.add_ema(df, 20)
        df = TechnicalIndicators.add_ema(df, 50)
        df = TechnicalIndicators.add_macd(df)
        df = TechnicalIndicators.add_rsi(df)
        df = TechnicalIndicators.add_bollinger_bands(df)
        df = TechnicalIndicators.add_volume_indicators(df)
        df = TechnicalIndicators.add_supertrend(df)
        return df
