import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import ccxt
import requests
from textblob import TextBlob

# Liste des sources alternatives pour éviter une surcharge
DATA_SOURCES = {
    "binance": "fetch_from_binance",
    "coingecko": "fetch_from_coingecko",
    "yahoo_finance": "fetch_from_yahoo",
    "nyse": "fetch_from_nyse",
    "indices": "fetch_from_indices",
    "swiss_market": "fetch_from_swiss_market",
    "reddit": "fetch_social_trends",
    "twitter": "fetch_social_trends"
}

# Fonction pour récupérer les prix depuis Binance
def fetch_from_binance(symbols):
    try:
        exchange = ccxt.binance()
        exchange.load_markets()
        prices = {symbol: exchange.fetch_ticker(symbol)['last'] for symbol in symbols}
        return prices
    except Exception as e:
        st.warning(f"⚠️ Binance inaccessible, utilisation d'une autre source. Erreur : {e}")
        return None

# Fonction pour récupérer les prix depuis CoinGecko
def fetch_from_coingecko(symbols):
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price",
                                params={"ids": ",".join([s.split("/")[0].lower() for s in symbols]),
                                        "vs_currencies": "usd"})
        data = response.json()
        return {symbol: data.get(symbol.split("/")[0].lower(), {}).get("usd", None) for symbol in symbols}
    except Exception as e:
        st.warning(f"⚠️ CoinGecko inaccessible, utilisation d'une autre source. Erreur : {e}")
        return None

# Fonction pour récupérer les prix des actions NYSE depuis Yahoo Finance
def fetch_from_nyse(symbols):
    try:
        base_url = "https://query1.finance.yahoo.com/v7/finance/quote"
        response = requests.get(base_url, params={"symbols": ",".join(symbols)})
        data = response.json()
        prices = {quote['symbol']: quote['regularMarketPrice'] for quote in data['quoteResponse']['result']}
        return prices
    except Exception as e:
        st.warning(f"⚠️ NYSE Data inaccessible, utilisation d'une autre source. Erreur : {e}")
        return None

# Fonction pour récupérer les indices boursiers populaires
def fetch_from_indices():
    try:
        indices = ["^GSPC", "^DJI", "^IXIC", "^FTSE", "^N225"]  # S&P 500, Dow Jones, Nasdaq, FTSE 100, Nikkei 225
        base_url = "https://query1.finance.yahoo.com/v7/finance/quote"
        response = requests.get(base_url, params={"symbols": ",".join(indices)})
        data = response.json()
        prices = {quote['symbol']: quote['regularMarketPrice'] for quote in data['quoteResponse']['result']}
        return prices
    except Exception as e:
        st.warning(f"⚠️ Indices boursiers inaccessibles. Erreur : {e}")
        return None

# Fonction pour récupérer les prix des Small & Mid Cap suisses et Nestlé
def fetch_from_swiss_market():
    try:
        swiss_stocks = ["NESN.SW", "LONN.SW", "GIVN.SW", "SREN.SW", "ZURN.SW"]  # Nestlé et autres Small/Mid Caps
        base_url = "https://query1.finance.yahoo.com/v7/finance/quote"
        response = requests.get(base_url, params={"symbols": ",".join(swiss_stocks)})
        data = response.json()
        prices = {quote['symbol']: quote['regularMarketPrice'] for quote in data['quoteResponse']['result']}
        return prices
    except Exception as e:
        st.warning(f"⚠️ Marché suisse inaccessible. Erreur : {e}")  # ✅ Correction ici (une seule ligne)
        return None

# Sélection intelligente de la source de données
def fetch_live_prices(symbols):
    for source in DATA_SOURCES:
        func = globals().get(DATA_SOURCES[source])
        if func:
            prices = func(symbols) if source not in ["indices", "swiss_market"] else func()
            if prices:
                return prices
    st.error("❌ Aucune source de données n'est accessible actuellement.")
    return {}

# Test des prix récupérés
st.subheader("Marchés Financiers : Crypto, NYSE, Indices Boursiers et Marché Suisse")
