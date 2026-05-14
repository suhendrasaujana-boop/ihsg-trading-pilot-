import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class UIComponents:
    
    @staticmethod
    def create_candlestick_chart(df, title="Price Chart"):
        """Create interactive candlestick chart"""
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.6, 0.2, 0.2],
            subplot_titles=(title, "RSI", "Volume")
        )
        
        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="Price"
            ),
            row=1, col=1
        )
        
        # Add EMA lines
        if 'ema_20' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['ema_20'], 
                          name="EMA 20", line=dict(color='orange', width=1)),
                row=1, col=1
            )
        
        if 'ema_50' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['ema_50'], 
                          name="EMA 50", line=dict(color='blue', width=1)),
                row=1, col=1
            )
        
        # Add Supertrend
        if 'supertrend' in df.columns:
            supertrend_up = df[df['supertrend_direction'] == 1]['supertrend']
            supertrend_down = df[df['supertrend_direction'] == -1]['supertrend']
            
            fig.add_trace(
                go.Scatter(x=supertrend_up.index, y=supertrend_up,
                          name="Supertrend Up", line=dict(color='green', width=1, dash='dot')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=supertrend_down.index, y=supertrend_down,
                          name="Supertrend Down", line=dict(color='red', width=1, dash='dot')),
                row=1, col=1
            )
        
        # RSI
        fig.add_trace(
            go.Scatter(x=df.index, y=df['rsi'], name="RSI", line=dict(color='purple')),
            row=2, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # Volume
        colors = ['red' if row['Open'] > row['Close'] else 'green' 
                  for idx, row in df.iterrows()]
        fig.add_trace(
            go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color=colors),
            row=3, col=1
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(rangeslider_visible=False)
        
        return fig
    
    @staticmethod
    def display_signal_card(signal_result, current_price):
        """Display trading signal in a nice card"""
        score = signal_result['total_score']
        signal = signal_result['signal']
        
        # Color coding
        if "STRONG BUY" in signal:
            color = "#00ff00"
            bg_color = "#1a3a1a"
            emoji = "🚀"
        elif "BUY" in signal:
            color = "#90ff90"
            bg_color = "#1a2a1a"
            emoji = "📈"
        elif "SELL" in signal:
            color = "#ff6666"
            bg_color = "#3a1a1a"
            emoji = "📉"
        else:
            color = "#ffff00"
            bg_color = "#2a2a1a"
            emoji = "⏸️"
        
        st.markdown(f"""
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid {color};
            margin: 10px 0;
        ">
            <h2 style="color: {color}; margin: 0;">
                {emoji} {signal} ({score}/100)
            </h2>
            <h4 style="color: white;">Current Price: Rp {current_price:,.2f}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display detailed signals
        with st.expander("📊 Detailed Signals", expanded=True):
            cols = st.columns(4)
            metrics = [
                ("Trend", signal_result['trend_score']),
                ("Momentum", signal_result['momentum_score']),
                ("Volume", signal_result['volume_score']),
                ("Volatility", signal_result['volatility_score'])
            ]
            
            for col, (name, value) in zip(cols, metrics):
                col.metric(name, f"{value}/100")
            
            st.write("**Key Signals:**")
            for sig in signal_result['signals']:
                st.write(f"• {sig}")
    
    @staticmethod
    def display_metrics(df):
        """Display key metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = df['Close'].iloc[-1]
        price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        
        col1.metric("Current Price", f"Rp {current_price:,.2f}", f"{price_change:.2f}%")
        col2.metric("RSI", f"{df['rsi'].iloc[-1]:.1f}")
        col3.metric("Volume Ratio", f"{df['volume_ratio'].iloc[-1]:.2f}x")
        col4.metric("ATR", f"Rp {df['atr'].iloc[-1]:.2f}")
