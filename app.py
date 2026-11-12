import os
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="AI EXCHANGE ALPHA",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 AI EXCHANGE ALPHA")
st.caption("Painel inteligente de análise de mercados")

st.info("Modo de demonstração: sem operações financeiras reais.")

# Configuração da CoinGecko
API_URL = "https://api.coingecko.com/api/v3"

def buscar_cotacoes():
   chave = os.getenv("COINGECKO_API_KEY", "")
    if not chave:
        raise Exception(
            "Chave não encontrada. Verifique o nome do segredo."
        )

    moedas = (
        "bitcoin,ethereum,solana,binancecoin,"
        "ripple,dogecoin,cardano"
    )

    resposta = requests.get(
        f"{API_URL}/simple/price",
        params={
            "ids": moedas,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        },
        headers={
            "x-cg-demo-api-key": chave
        },
        timeout=20
    )

    resposta.raise_for_status()
    return resposta.json()


@st.cache_data(ttl=30)
def carregar_cotacoes():
    return buscar_cotacoes()


st.subheader("📈 Mercado de criptomoedas")

if st.button("🔄 Atualizar cotações"):
    carregar_cotacoes.clear()

try:
    dados = carregar_cotacoes()

    lista = [
        ("Bitcoin", "bitcoin", "BTC"),
        ("Ethereum", "ethereum", "ETH"),
        ("Solana", "solana", "SOL"),
        ("BNB", "binancecoin", "BNB"),
        ("XRP", "ripple", "XRP"),
        ("Dogecoin", "dogecoin", "DOGE"),
        ("Cardano", "cardano", "ADA")
    ]

    colunas = st.columns(2)

    for i, (nome, id_moeda, simbolo) in enumerate(lista):
        with colunas[i % 2]:
            preco = dados[id_moeda]["usd"]
            variacao = dados[id_moeda].get(
                "usd_24h_change", 0
            )

            st.metric(
                f"{nome} ({simbolo})",
                f"US$ {preco:,.4f}",
                f"{variacao:+.2f}%"
            )

    st.caption(
        "Última consulta: " +
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

except Exception as erro:
    st.error(f"Erro ao buscar cotações: {erro}")

st.divider()

st.subheader("🧪 Simulador de investimento")

capital = st.number_input(
    "Capital fictício (US$)",
    min_value=100.0,
    value=10000.0,
    step=100.0
)

variacao = st.slider(
    "Variação simulada (%)",
    -20.0, 20.0, 0.0, 0.5
)

resultado = capital * (1 + variacao / 100)

st.metric(
    "Saldo simulado",
    f"US$ {resultado:,.2f}",
    f"{variacao:+.1f}%"
)

st.warning(
    "Simulação educativa. Não executa compras ou vendas."
)
