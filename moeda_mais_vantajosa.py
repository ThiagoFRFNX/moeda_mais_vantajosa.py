import streamlit as st
import requests

st.set_page_config(page_title="Conversor de Viagem", page_icon="🌍")

st.title("💱 Comparador de Preço: Peso vs Dólar")
st.markdown("Informe os preços em **pesos argentinos** e **dólares**, e veja qual é mais vantajoso pagar, com base na cotação atual.")

# Entrada do usuário
preco_pesos = st.number_input("Preço em pesos argentinos (ARS)", min_value=0.0, step=0.01)
preco_dolares = st.number_input("Preço em dólares (USD)", min_value=0.0, step=0.01)

# Função para obter cotações com tratamento de erro
@st.cache_data
def obter_cotacoes():
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,ARS-BRL"
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()  # Erro se status HTTP não for 200
        dados = resposta.json()

        # Verifica se a resposta contém os dados esperados
        if 'USDBRL' not in dados or 'ARSBRL' not in dados:
            st.error("⚠️ A resposta da API está em formato inesperado.")
            st.json(dados)  # Mostra o JSON retornado para debug
            return None, None

        cotacao_usd = float(dados['USDBRL']['bid'])
        cotacao_ars = float(dados['ARSBRL']['bid'])
        return cotacao_usd, cotacao_ars

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro de conexão com a API: {e}")
        return None, None
    except Exception as e:
        st.error(f"❌ Erro ao processar os dados da API: {e}")
        return None, None

# Botão para calcular
if st.button("Calcular melhor opção"):
    cotacao_usd, cotacao_ars = obter_cotacoes()

    if cotacao_usd is None or cotacao_ars is None:
        st.warning("⚠️ Não foi possível obter as cotações.")
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
