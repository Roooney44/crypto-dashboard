import streamlit as st import requests import ccxt import time from datetime import datetime

st.title("📊 Dashboard Marchés Financiers et Vérification")

# Définition des horaires d'ouverture et de fermeture du marché

MARKET_OPEN_HOUR = 9  # 9h00 (UTC) MARKET_CLOSE_HOUR = 21  # 21h00 (UTC)

Fonction pour vérifier si on est à l'ouverture ou à la fermeture du marché

def is_market_time(): current_hour = datetime.utcnow().hour return current_hour == MARKET_OPEN_HOUR or current_hour == MARKET_CLOSE_HOUR

Cache pour limiter les appels API

CACHE = {}

def get_cached_response(key): return CACHE.get(key)

def set_cached_response(key, data): CACHE[key] = data

Vérification de Binance API avec fallback sur CoinGecko

def check_binance(): try: exchange = ccxt.binance() exchange.load_markets() ticker = exchange.fetch_ticker("BTC/USDT") return {"status": "✅ Binance fonctionne", "BTC/USDT": ticker['last']} except Exception as e: return {"status": f"❌ Binance API Error: {e}, bascule vers CoinGecko"}

Vérification de CoinGecko API

def check_coingecko(): try: response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "bitcoin,ethereum", "vs_currencies": "usd"}) data = response.json() return {"status": "✅ CoinGecko fonctionne", "prices": data} except Exception as e: return {"status": f"❌ CoinGecko API Error: {e}"}

Vérification de Yahoo Finance API

def check_yahoo(): try: response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote", params={"symbols": "AAPL,TSLA,MSFT"}) if response.status_code != 200: return {"status": f"❌ Yahoo Finance API Error: HTTP {response.status_code}"} data = response.json() return {"status": "✅ Yahoo Finance fonctionne", "prices": data} except Exception as e: return {"status": f"❌ Yahoo Finance API Error: {e}"}

Vérification des indices boursiers

def check_indices(): try: indices = ["^GSPC", "^DJI", "^IXIC", "^FTSE", "^N225"] response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote", params={"symbols": ",".join(indices)}) if response.status_code != 200: return {"status": f"❌ Indices API Error: HTTP {response.status_code}"} data = response.json() return {"status": "✅ Indices boursiers fonctionnent", "prices": data} except Exception as e: return {"status": f"❌ Indices API Error: {e}"}

Exécution des vérifications à l'ouverture du dashboard et aux horaires du marché

verification_results = { "Binance API": check_binance(), "CoinGecko API": check_coingecko(), "Yahoo Finance API": check_yahoo(), "Indices Boursiers": check_indices() }

Mise en cache des résultats uniquement si c'est l'heure du marché

if is_market_time(): set_cached_response("market_data", verification_results)

Vérifier si on a des données en cache et les afficher si ce n'est pas l'heure du marché

cached_data = get_cached_response("market_data") if not is_market_time() and cached_data: verification_results = cached_data st.subheader("🔍 Résultats de la dernière mise à jour aux horaires du marché") else: st.subheader("🔍 Résultats de la mise à jour en direct")

Affichage des résultats

st.write(verification_results)

