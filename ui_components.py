import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class UIComponents:
    
    @staticmethod
    def apply_light_theme():
        """Apply light theme permanently"""
        st.markdown("""
        <style>
            /* Main background */
            .stApp {
                background-color: #ffffff !important;
            }
            
            /* Text color */
            .stMarkdown, .stText, .stTitle, .stSubtitle, .stHeader {
                color: #1a1a1a !important;
            }
            
            /* Sidebar */
            .css-1d391kg, .stSidebar {
                background-color: #f8f9fa !important;
            }
            
            /* Metric cards */
            [data-testid="stMetricValue"] {
                color: #1a1a1a !important;
            }
            
            [data-testid="stMetricLabel"] {
                color: #666666 !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                color: #1a1a1a !important;
                background-color: #f8f9fa !important;
            }
            
            /* Select box */
            .stSelectbox label {
                color: #1a1a1a !important;
            }
            
            /* Info box */
            .stAlert {
                background-color: #e3f2fd !important;
                color: #1a1a1a !important;
            }
            
            /* Dataframe */
            .stDataFrame {
                background-color: #ffffff !important;
            }
            
            /* Input field */
            .stTextInput label {
                color: #1a1a1a !important;
            }
            
            /* Button */
            .stButton button {
                background-color: #0066cc !important;
                color: white !important;
            }
            
            /* Chart background */
            .js-plotly-plot {
                background-color: #ffffff !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_candlestick_chart(df, title="Price Chart"):
        """Create interactive candlestick chart - fixed width parameter"""
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
        
        # Volume - fixed color logic
        colors = []
        for i in range(len(df)):
            if df['Open'].iloc[i] > df['Close'].iloc[i]:
                colors.append('red')
            else:
                colors.append('green')
        
        fig.add_trace(
            go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color=colors),
            row=3, col=1
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            height=800,
            showlegend=True,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_yaxes(gridcolor='#e0e0e0', gridwidth=0.5)
        
        return fig
    
    @staticmethod
    def display_signal_card(signal_result, current_price):
        """Display trading signal in a nice card - fixed width parameter"""
        score = signal_result['total_score']
        signal = signal_result['signal']
        
        # Color coding for light theme
        if "STRONG BUY" in signal:
            color = "#00a800"
            bg_color = "#e8f5e8"
            emoji = "🚀"
        elif "BUY" in signal:
            color = "#008800"
            bg_color = "#f0f9f0"
            emoji = "📈"
        elif "SELL" in signal:
            color = "#cc0000"
            bg_color = "#fee8e8"
            emoji = "📉"
        else:
            color = "#ff9900"
            bg_color = "#fff4e6"
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
                {emoji} {signal} ({score:.2f}/100)
            </h2>
            <h4 style="color: #1a1a1a;">Current Price: Rp {current_price:,.2f}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display detailed signals
        with st.expander("📊 Detailed Signals", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            metrics = [
                ("Trend", signal_result['trend_score']),
                ("Momentum", signal_result['momentum_score']),
                ("Volume", signal_result['volume_score']),
                ("Volatility", signal_result['volatility_score'])
            ]
            
            for col, (name, value) in zip([col1, col2, col3, col4], metrics):
                if value >= 50:
                    color = "green"
                elif value <= -30:
                    color = "red"
                else:
                    color = "orange"
                col.markdown(f"**{name}**<br><span style='color:{color};font-size:24px;font-weight:bold;'>{value:.1f}</span>", unsafe_allow_html=True)
            
            st.write("**Key Signals:**")
            for sig in signal_result['signals']:
                st.write(f"• {sig}")
    
    @staticmethod
    def display_metrics(df):
        """Display key metrics - fixed width parameter"""
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = df['Close'].iloc[-1]
        price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        change_color = "green" if price_change >= 0 else "red"
        change_sign = "+" if price_change >= 0 else ""
        
        col1.markdown(f"**Current Price**<br><span style='font-size:28px;'>Rp {current_price:,.0f}</span><br><span style='color:{change_color};'>{change_sign}{price_change:.2f}%</span>", unsafe_allow_html=True)
        col2.markdown(f"**RSI (14)**<br><span style='font-size:28px;'>{df['rsi'].iloc[-1]:.1f}</span>", unsafe_allow_html=True)
        col3.markdown(f"**Volume Ratio**<br><span style='font-size:28px;'>{df['volume_ratio'].iloc[-1]:.2f}x</span>", unsafe_allow_html=True)
        col4.markdown(f"**ATR**<br><span style='font-size:28px;'>Rp {df['atr'].iloc[-1]:.0f}</span>", unsafe_allow_html=True)
