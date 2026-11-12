
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AI EXCHANGE ALPHA",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 AI EXCHANGE ALPHA")
st.caption("Painel inteligente de análise e simulação de mercados")

st.info("Modo de demonstração: análise de mercado, sem operações reais.")

def buscar_preco(simbolo):
    url = "https://api.binance.com/api/v3/ticker/price"
    resposta = requests.get(
        url,
        params={"symbol": simbolo},
        timeout=10
    )
    resposta.raise_for_status()
    return float(resposta.json()["price"])

st.subheader("📈 Mercado de criptomoedas")

if st.button("🔄 Atualizar cotações"):
    st.cache_data.clear()

@st.cache_data(ttl=30)
def carregar_cotacoes():
    dados = {}
    for moeda in ["BTCUSDT", "ETHUSDT"]:
        try:
            dados[moeda] = buscar_preco(moeda)
        except Exception:
            dados[moeda] = None
    return dados

dados = carregar_cotacoes()

col1, col2 = st.columns(2)

with col1:
    if dados["BTCUSDT"] is not None:
        st.metric("Bitcoin (BTC)", f"US$ {dados['BTCUSDT']:,.2f}")
    else:
        st.warning("Cotação do Bitcoin indisponível.")

with col2:
    if dados["ETHUSDT"] is not None:
        st.metric("Ethereum (ETH)", f"US$ {dados['ETHUSDT']:,.2f}")
    else:
        st.warning("Cotação do Ethereum indisponível.")

st.divider()

st.subheader("🧪 Simulador de investimento")

capital = st.number_input(
    "Capital fictício (US$)",
    min_value=100.0,
    value=10000.0,
    step=100.0
)

variacao = st.slider(
    "Simular variação do mercado (%)",
    min_value=-20.0,
    max_value=20.0,
    value=0.0,
    step=0.5
)

resultado = capital * (1 + variacao / 100)

st.metric(
    "Saldo simulado",
    f"US$ {resultado:,.2f}",
    f"{variacao:+.1f}%"
)

st.caption(
    "Última consulta: " +
    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
)

st.warning(
    "Simulação educativa. Não representa recomendação "
    "financeira nem executa compras ou vendas."
)
