import streamlit as st
import requests
import ccxt

st.title("📊 Dashboard de Vérification des Données")

# Vérification de Binance API
def check_binance():
    try:
        exchange = ccxt.binance()
        exchange.load_markets()
        ticker = exchange.fetch_ticker("BTC/USDT")
        return {"status": "✅ Binance fonctionne", "BTC/USDT": ticker['last']}
    except Exception as e:
        return {"status": f"❌ Binance API Error: {e}"}

# Vérification de CoinGecko API
def check_coingecko():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price",
                                params={"ids": "bitcoin,ethereum", "vs_currencies": "usd"})
        data = response.json()
        return {"status": "✅ CoinGecko fonctionne", "prices": data}
    except Exception as e:
        return {"status": f"❌ CoinGecko API Error: {e}"}

# Vérification de Yahoo Finance API
def check_yahoo():
    try:
        response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote",
                                params={"symbols": "AAPL,TSLA,MSFT"})
        data = response.json()
        return {"status": "✅ Yahoo Finance fonctionne", "prices": data}
    except Exception as e:
        return {"status": f"❌ Yahoo Finance API Error: {e}"}

# Vérification des indices boursiers
def check_indices():
    try:
        indices = ["^GSPC", "^DJI", "^IXIC", "^FTSE", "^N225"]
        response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote",
                                params={"symbols": ",".join(indices)})
        data = response.json()
        return {"status": "✅ Indices boursiers fonctionnent", "prices": data}
    except Exception as e:
        return {"status": f"❌ Indices API Error: {e}"}

# Exécution des vérifications
verification_results = {
    "Binance API": check_binance(),
    "CoinGecko API": check_coingecko(),
    "Yahoo Finance API": check_yahoo(),
    "Indices Boursiers": check_indices()
}

# Ajout de l'affichage après la définition des résultats
st.subheader("🔍 Résultats de la vérification des API")
st.write(verification_results)
