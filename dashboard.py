import streamlit as st import pandas as pd import numpy as np import time import plotly.express as px

Simulated trading data

def generate_data(): return pd.DataFrame({ 'Timestamp': pd.date_range(start='2024-01-01', periods=100, freq='T'), 'Price': np.cumsum(np.random.randn(100)) + 30000, 'Balance': np.cumsum(np.random.randn(100) * 10) + 10000, 'Trades': np.random.randint(0, 2, 100) })

data = generate_data()

st.title("Crypto Trading Dashboard")

Live Price Chart

st.subheader("Live Price Movement") fig_price = px.line(data, x='Timestamp', y='Price', title='Crypto Price Over Time') st.plotly_chart(fig_price)

Balance Over Time

st.subheader("Account Balance Over Time") fig_balance = px.line(data, x='Timestamp', y='Balance', title='Balance Evolution') st.plotly_chart(fig_balance)

Trade Activity

st.subheader("Trade Actions") fig_trades = px.bar(data, x='Timestamp', y='Trades', title='Buy/Sell Actions') st.plotly_chart(fig_trades)

Live Data Simulation

st.subheader("Live Data Update") latest_price = st.empty() for i in range(10): new_price = np.random.randn() * 100 + 30000 latest_price.metric(label="Current Crypto Price", value=f"${new_price:.2f}") time.sleep(2)

