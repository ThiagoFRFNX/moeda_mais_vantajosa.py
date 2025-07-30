import streamlit as st
import requests

st.set_page_config(page_title="Conversor de Viagem", page_icon="🌍")

st.title("💱 Comparador de Preço: Peso vs Dólar")
st.markdown("Informe os preços em **pesos argentinos** e **dólares**, e veja qual é mais vantajoso pagar, com base na cotação atual.")

# Entrada do usuário
preco_pesos = st.number_input("Preço em pesos argentinos (ARS)", min_value=0.0, step=0.01)
preco_dolares = st.number_input("Preço em dólares (USD)", min_value=0.0, step=0.01)

# Função para obter cotações
@st.cache_data
def obter_cotacoes():
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,ARS-BRL"
        resposta = requests.get(url)
        dados = resposta.json()
        cotacao_usd = float(dados['USDBRL']['bid'])
        cotacao_ars = float(dados['ARSBRL']['bid'])
        return cotacao_usd, cotacao_ars
    except:
        return None, None

# Botão para calcular
if st.button("Calcular melhor opção"):
    cotacao_usd, cotacao_ars = obter_cotacoes()

    if cotacao_usd is None:
        st.error("Erro ao buscar cotações.")
    else:
        valor_em_reais_pesos = preco_pesos * cotacao_ars
        valor_em_reais_dolares = preco_dolares * cotacao_usd

        st.subheader("📈 Cotações do dia")
        st.write(f"1 USD = R$ {cotacao_usd:.2f}")
        st.write(f"1 ARS = R$ {cotacao_ars:.4f}")

        st.subheader("💰 Comparação de valores")
        st.write(f"Pagando em **pesos**: R$ {valor_em_reais_pesos:.2f}")
        st.write(f"Pagando em **dólares**: R$ {valor_em_reais_dolares:.2f}")

        st.subheader("🔎 Resultado:")
        if valor_em_reais_pesos < valor_em_reais_dolares:
            st.success("✅ Mais vantajoso pagar em **PESOS**.")
        elif valor_em_reais_pesos > valor_em_reais_dolares:
            st.success("✅ Mais vantajoso pagar em **DÓLARES**.")
        else:
            st.info("⚖️ Tanto faz — os valores são iguais.")