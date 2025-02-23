import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import ccxt  # Import de ccxt pour récupérer les prix du marché en temps réel
import requests  # Pour récupérer les tendances de Reddit, Twitter, et analyses financières
from textblob import TextBlob  # Analyse de sentiment

# Connexion à Binance pour récupérer les prix en temps réel des 10 meilleures cryptos
def fetch_live_prices(symbols=["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT",
                               "SOL/USDT", "DOGE/USDT", "DOT/USDT", "MATIC/USDT", "LTC/USDT"]):
    exchange = ccxt.binance()
    prices = {}
    for symbol in symbols:
        ticker = exchange.fetch_ticker(symbol)
        prices[symbol] = ticker['last']
    return prices

# Récupération des tendances Twitter, Reddit et analyse de sentiment
def fetch_social_trends():
    reddit_trends = requests.get("https://www.reddit.com/r/cryptocurrency/top.json?limit=5",
                                 headers={'User-Agent': 'Mozilla/5.0'}).json()
    twitter_trends = requests.get("https://api.coingecko.com/api/v3/search/trending").json()
    
    reddit_posts = [post['data']['title'] for post in reddit_trends['data']['children']]
    twitter_coins = [coin['item']['name'] for coin in twitter_trends['coins']]
    
    # Calcul du score de sentiment
    reddit_sentiments = [TextBlob(post).sentiment.polarity for post in reddit_posts]
    avg_sentiment = np.mean(reddit_sentiments) if reddit_sentiments else 0

    return reddit_posts, twitter_coins, avg_sentiment

# Récupération des analyses financières depuis GuruFocus, Yahoo Finance et Google Finance
def fetch_financial_analysis():
    yahoo_finance = requests.get("https://query1.finance.yahoo.com/v1/finance/trending/US").json()
    guru_focus = requests.get("https://www.gurufocus.com/news/latest").json()
    google_finance = requests.get("https://www.google.com/finance/markets/news").json()
    
    yahoo_trends = [item['symbol'] for item in yahoo_finance.get('finance', {}).get('result', [{}])[0].get('quotes', [])]
    guru_articles = [article['title'] for article in guru_focus.get('articles', [])[:5]]
    google_news = [news['title'] for news in google_finance.get('stories', [])[:5]]

    return yahoo_trends, guru_articles, google_news

# Génération de données de trading dynamiques
def generate_data():
    timestamps = pd.date_range(start='2024-01-01', periods=100, freq='T')
    live_prices = fetch_live_prices()
    df_list = []
    for symbol, price in live_prices.items():
        prices = price + np.cumsum(np.random.randn(100) * 10)
        balance = 10000 + np.cumsum(np.random.randn(100) * 10)
        trades = np.random.randint(0, 2, 100)
        df = pd.DataFrame({'Timestamp': timestamps, 'Price': prices, 'Balance': balance, 'Trades': trades, 'Crypto': symbol})
        df_list.append(df)
    return pd.concat(df_list)

data = generate_data()

st.title("Crypto Trading Dashboard - Top 10 Cryptos")

# Live Price Charts
st.subheader("Live Price Movement for Top 10 Cryptos")
fig_price = px.line(data, x='Timestamp', y='Price', color='Crypto', title='Crypto Prices Over Time')
st.plotly_chart(fig_price)

# Balance Over Time
st.subheader("Account Balance Over Time")
fig_balance = px.line(data, x='Timestamp', y='Balance', color='Crypto', title='Balance Evolution')
st.plotly_chart(fig_balance)

# Trade Activity
st.subheader("Trade Actions")
fig_trades = px.bar(data, x='Timestamp', y='Trades', color='Crypto', title='Buy/Sell Actions')
st.plotly_chart(fig_trades)

# Live Data Update for Top 10 Cryptos
st.subheader("Live Market Data")
latest_prices = st.empty()
for i in range(10):
    new_prices = fetch_live_prices()
    latest_prices.write(pd.DataFrame(new_prices.items(), columns=["Crypto", "Price"]))
    time.sleep(2)

# Trending topics from Reddit and Twitter with Sentiment Analysis
st.subheader("Social Media Trends & Sentiment Analysis")
reddit_posts, twitter_coins, avg_sentiment = fetch_social_trends()
st.write("### 🔥 Top Reddit Posts:")
for post in reddit_posts:
    st.write(f"- {post}")

st.write("### 📢 Trending Coins on Twitter:")
st.write(", ".join(twitter_coins))

# Sentiment Indicator
st.subheader("📊 Sentiment Analysis Score")
sentiment_status = "🔴 Negative" if avg_sentiment < -0.2 else "🟡 Neutral" if avg_sentiment < 0.2 else "🟢 Positive"
st.metric(label="Reddit Sentiment Score", value=f"{avg_sentiment:.2f}", delta=sentiment_status)

# Financial Analysis Summary
st.subheader("📈 Financial Market Insights")
yahoo_trends, guru_articles, google_news = fetch_financial_analysis()
st.write("### 📊 Yahoo Finance Trending Stocks:")
st.write(", ".join(yahoo_trends))

st.write("### 📰 GuruFocus Latest Analysis:")
for article in guru_articles:
    st.write(f"- {article}")

st.write("### 📰 Google Finance Market News:")
for news in google_news:
    st.write(f"- {news}")

st.write("🚀 Application Streamlit connectée au marché en temps réel avec Binance + Social Trends de Reddit, Twitter et analyses financières (GuruFocus, Yahoo Finance, Google Finance) ! 🎉")
