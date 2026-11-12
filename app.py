
import streamlit as st
import requests
import os
from datetime import datetime

# CONFIGURAÇÃO
st.set_page_config(
    page_title="AI EXCHANGE ALPHA",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 AI EXCHANGE ALPHA")
st.caption("Painel inteligente de análise de mercados")

st.info(
    "Modo de demonstração: análise de mercado, "
    "sem operações financeiras reais."
)

# CHAVE DA COINGECKO
def obter_chave():
    return os.getenv("COINGECKO_API_KEY", "")


# BUSCAR COTAÇÕES
def buscar_cotacoes():

    chave = obter_chave()

    if not chave:
        raise Exception(
            "Chave não encontrada. Verifique "
            "COINGECKO_API_KEY nos Secrets."
        )

    moedas = (
        "bitcoin,ethereum,solana,binancecoin,"
        "ripple,dogecoin,cardano"
    )

    url = "https://api.coingecko.com/api/v3/simple/price"

    resposta = requests.get(
        url,
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

    if resposta.status_code != 200:
        raise Exception(
            f"Erro da CoinGecko: HTTP {resposta.status_code} "
            f"- {resposta.text[:300]}"
        )

    return resposta.json()


# CACHE
@st.cache_data(ttl=30)
def carregar_cotacoes():
    return buscar_cotacoes()


# MERCADO
st.subheader("📈 Mercado de criptomoedas")

if st.button("🔄 Atualizar cotações"):
    carregar_cotacoes.clear()

lista_moedas = [
    ("Bitcoin", "bitcoin", "BTC"),
    ("Ethereum", "ethereum", "ETH"),
    ("Solana", "solana", "SOL"),
    ("BNB", "binancecoin", "BNB"),
    ("XRP", "ripple", "XRP"),
    ("Dogecoin", "dogecoin", "DOGE"),
    ("Cardano", "cardano", "ADA")
]

try:
    dados = carregar_cotacoes()

    colunas = st.columns(2)

    for i, (nome, identificador, simbolo) in enumerate(lista_moedas):

        with colunas[i % 2]:

            if identificador in dados:

                preco = dados[identificador]["usd"]

                variacao = dados[identificador].get(
                    "usd_24h_change", 0
                )

                st.metric(
                    f"{nome} ({simbolo})",
                    f"US$ {preco:,.4f}",
                    f"{variacao:+.2f}%"
                )

            else:
                st.warning(
                    f"Dados indisponíveis: {nome}"
                )

    st.caption(
        "Última consulta: "
        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

except Exception as erro:
    st.error(f"Não foi possível carregar as cotações: {erro}")

st.divider()

# SIMULADOR
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

st.divider()

st.caption(
    "AI EXCHANGE ALPHA - Versão de desenvolvimento."
)

st.warning(
    "Simulação educativa. Não representa recomendação "
    "financeira nem executa compras ou vendas."
)
