import pandas as pd
import numpy as np

class ScoringEngine:
    
    def __init__(self, weights=None):
        self.weights = weights or {
            'trend': 0.35,
            'momentum': 0.30,
            'volume': 0.20,
            'volatility': 0.15
        }
    
    def calculate_trend_score(self, df):
        """Evaluate trend strength"""
        score = 0
        signals = []
        
        # EMA alignment
        if df['ema_20'].iloc[-1] > df['ema_50'].iloc[-1]:
            score += 30
            signals.append("EMA Bullish")
        else:
            score -= 20
            signals.append("EMA Bearish")
        
        # MACD
        if df['macd'].iloc[-1] > df['macd_signal'].iloc[-1]:
            score += 25
            signals.append("MACD Bullish")
        else:
            score -= 15
            signals.append("MACD Bearish")
        
        # Supertrend
        if df['supertrend_direction'].iloc[-1] == 1:
            score += 25
            signals.append("Supertrend Up")
        else:
            score -= 20
            signals.append("Supertrend Down")
        
        # Price vs EMA 20
        if df['Close'].iloc[-1] > df['ema_20'].iloc[-1]:
            score += 20
            signals.append("Above EMA20")
        else:
            score -= 15
            signals.append("Below EMA20")
        
        return np.clip(score, -100, 100), signals
    
    def calculate_momentum_score(self, df):
        """Evaluate momentum"""
        score = 0
        signals = []
        
        rsi = df['rsi'].iloc[-1]
        
        # RSI
        if rsi < 30:
            score += 40
            signals.append(f"RSI Oversold ({rsi:.1f})")
        elif rsi > 70:
            score -= 40
            signals.append(f"RSI Overbought ({rsi:.1f})")
        elif 40 <= rsi <= 60:
            score += 10
            signals.append("RSI Neutral")
        
        # Price momentum
        if len(df) >= 6:
            price_change = (df['Close'].iloc[-1] - df['Close'].iloc[-6]) / df['Close'].iloc[-6] * 100
            if price_change > 2:
                score += 30
                signals.append(f"Strong Momentum (+{price_change:.1f}%)")
            elif price_change < -2:
                score -= 30
                signals.append(f"Strong Down Momentum ({price_change:.1f}%)")
        
        # MACD cross
        if len(df) >= 2:
            if df['macd_diff'].iloc[-1] > 0 and df['macd_diff'].iloc[-2] <= 0:
                score += 30
                signals.append("MACD Bullish Cross")
            elif df['macd_diff'].iloc[-1] < 0 and df['macd_diff'].iloc[-2] >= 0:
                score -= 30
                signals.append("MACD Bearish Cross")
        
        return np.clip(score, -100, 100), signals
    
    def calculate_volume_score(self, df):
        """Evaluate volume pattern"""
        score = 0
        signals = []
        
        volume_ratio = df['volume_ratio'].iloc[-1]
        
        # Volume spike
        if volume_ratio > 1.5:
            if df['Close'].iloc[-1] > df['Close'].iloc[-2]:
                score += 40
                signals.append(f"High Volume Up ({volume_ratio:.1f}x)")
            else:
                score -= 30
                signals.append(f"High Volume Down ({volume_ratio:.1f}x)")
        elif volume_ratio < 0.5:
            signals.append("Low Volume")
        
        # Volume trend
        if len(df) >= 20:
            volume_trend = (df['Volume'].iloc[-5:].mean() / df['Volume'].iloc[-20:].mean())
            if volume_trend > 1.2:
                score += 30
                signals.append("Increasing Volume Trend")
        
        return np.clip(score, -100, 100), signals
    
    def calculate_volatility_score(self, df):
        """Evaluate volatility conditions"""
        score = 0
        signals = []
        
        # Bollinger Bands position
        current_price = df['Close'].iloc[-1]
        bb_lower = df['bb_lower'].iloc[-1]
        bb_upper = df['bb_upper'].iloc[-1]
        bb_middle = df['bb_middle'].iloc[-1]
        
        bb_width = (bb_upper - bb_lower) / bb_middle if bb_middle != 0 else 0
        
        if current_price <= bb_lower:
            score += 40
            signals.append("At Lower BB (Potential Bounce)")
        elif current_price >= bb_upper:
            score -= 30
            signals.append("At Upper BB (Potential Pullback)")
        
        # Squeeze detection
        if bb_width < 0.05:
            signals.append("BB Squeeze (Volatility Coming)")
            score += 20
        
        # ATR trend
        if len(df) >= 6 and df['atr'].iloc[-6] != 0:
            atr_change = (df['atr'].iloc[-1] - df['atr'].iloc[-6]) / df['atr'].iloc[-6] * 100
            if atr_change > 20:
                signals.append("Increasing Volatility")
        
        return np.clip(score, -100, 100), signals
    
    def calculate_total_score(self, df):
        """Calculate total weighted score"""
        trend_score, trend_signals = self.calculate_trend_score(df)
        momentum_score, momentum_signals = self.calculate_momentum_score(df)
        volume_score, volume_signals = self.calculate_volume_score(df)
        volatility_score, volatility_signals = self.calculate_volatility_score(df)
        
        total_score = (
            trend_score * self.weights['trend'] +
            momentum_score * self.weights['momentum'] +
            volume_score * self.weights['volume'] +
            volatility_score * self.weights['volatility']
        )
        
        all_signals = trend_signals + momentum_signals + volume_signals + volatility_signals
        
        # Determine signal
        if total_score >= 70:
            signal = "STRONG BUY 🚀"
        elif total_score >= 50:
            signal = "BUY 📈"
        elif total_score >= 30:
            signal = "WATCH / ACCUMULATE ⏸️"
        elif total_score >= 10:
            signal = "NEUTRAL"
        elif total_score >= -10:
            signal = "WATCH / DISTRIBUTE"
        elif total_score >= -30:
            signal = "SELL 📉"
        else:
            signal = "STRONG SELL 🔻"
        
        return {
            'total_score': round(total_score, 2),
            'trend_score': round(trend_score, 2),
            'momentum_score': round(momentum_score, 2),
            'volume_score': round(volume_score, 2),
            'volatility_score': round(volatility_score, 2),
            'signal': signal,
            'signals': all_signals[:8]
        }
