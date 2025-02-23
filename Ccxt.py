import streamlit as st
try:
    import ccxt
    st.write("✅ ccxt est bien installé")
except ModuleNotFoundError:
    st.write("❌ ccxt n'est pas installé")
