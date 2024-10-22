import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

query = "SELECT * FROM tb_carro"

df = conexao(query)

if st.button("Atualizar Dados"):
    df = conexao(query)

st.sidebar.header("Selecione o Filtro")

nome = st.sidebar.multiselect(
    "Marca Selecionada",
    options=df["nome"].unique(),
    default=df["nome"].unique()
)

modelo = st.sidebar.multiselect(
    "Modelo Selecionado",
    options=df["modelo"].unique(),
    default=df["modelo"].unique()
)

min_ano = df["ano"].min()
max_ano = df["ano"].max()
ano = st.sidebar.slider(
    "Selecione um intervalo de anos",
    min_value=min_ano,
    max_value=max_ano,
    value=(min_ano, max_ano)
)

min_valor = df["valor"].min()
max_valor = df["valor"].max()
valor = st.sidebar.slider(
    "Selecione o intervalo de valores",
    min_value=min_valor,
    max_value=max_valor,
    value=(min_valor, max_valor)
)

cor = st.sidebar.multiselect(
    "Cor Selecionada",
    options=df["cor"].unique(),
    default=df["cor"].unique()
)

min_vendas = df["numero_vendas"].min()
max_vendas = df["numero_vendas"].max()
vendas = st.sidebar.slider(
    "Selecione o intervalo de vendas",
    min_value=min_vendas,
    max_value=max_vendas,
    value=(min_vendas, max_vendas)
)

filtro  = df[
    (df["nome"].isin(nome)) &
    (df["modelo"].isin(modelo)) &
    (df["cor"].isin(cor)) & 
    df["valor"].between(valor[0], valor[1]) &
    df["ano"].between(ano[0], ano[1]) &
    df["numero_vendas"].between(vendas[0], vendas[1])
]

def Home():
    with st.expander("Valores"):
        mostrar_dados = st.multiselect("Filter: ", filtro, default=[])

        if mostrar_dados:
            st.write(filtro[mostrar_dados])
    if not filtro.empty:
        venda_total = filtro["numero_vendas"].sum()
        venda_media = filtro["numero_vendas"].mean()
        venda_mediana = filtro["numero_vendas"].median()
        venda_min = filtro["numero_vendas"].min()
        venda_max = filtro["numero_vendas"].max()

        total1, total2, total3 = st.columns(3, gap="large")
        
        with total1:
            st.info("Valor total de vendas dos Carros", icon="❕")
            st.metric(label="Total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("Valor médio das vendas", icon="❕")
            st.metric(label="Média", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Valor mediano dos Carros", icon="❕")
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")
    else:
        st.warning("Nenhum dados disponivel para filtrar")


    st.markdown("""---------""")

def graficos(filtro):
    if filtro.empty:
        st.warning("Nenhum dado disponivel para gerar graficos")
        return 

    graf1, graf2, graf3, graf4 = st.tabs([
        "Gráfico de Barras", 
        "Gráfico de Linhas",
        "Gráfico de Pizza", 
        "Gráfico de Dispersao"
    ])


Home()