import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Dashboard de Segurança Pública",
    layout="wide"
)

# ==================================================
# LEITURA DOS DADOS
# ==================================================
arquivos = {
    "2019": "crimes_violentos_2019.csv",
    "2020": "crimes_violentos_2020.csv",
    "2021": "crimes_violentos_2021.csv",
    "2022": "crimes_violentos_2022.csv",
    "2023": "crimes_violentos_2023.csv",
    "2024": "crimes_violentos_2024.csv",
    "2025": "crimes_violentos_2025.csv",
    "2026": "crimes_violentos_2026.csv"
}

dfs = []

for arquivo in arquivos.values():
    temp = pd.read_csv(
        arquivo,
        sep=";"
    )

    dfs.append(temp)

df = pd.concat(
    dfs,
    ignore_index=True
)





# ==================================================
# SIDEBAR (FILTROS)
# ==================================================

st.sidebar.title("Filtros")

ano = st.sidebar.selectbox(
    "Ano",
    sorted(df["ano"].unique())
)

municipios = ["Todos"] + sorted(
    df["municipio"].unique()
)

municipio = st.sidebar.selectbox(
    "Município",
    municipios
)

# Aplicação dos filtros

df = df[df["ano"] == ano]

if municipio != "Todos":
    df = df[df["municipio"] == municipio]

df = df[df["ano"] == ano]

# ==================================================
# CABEÇALHO
# ==================================================

st.title("Dashboard de Crimes Violentos em Minas Gerais")

st.write(
    "Análise de registros de crimes violentos."
)

st.markdown("---")

# ==================================================
# KPIs
# ==================================================

col1, col2, col3 = st.columns(3)

total_crimes = df["registros"].sum()

total_municipios = df["municipio"].nunique()

crime_mais_comum = (
    df.groupby("natureza")["registros"]
    .sum()
    .idxmax()
)

col1.metric(
    "Total de Crimes",
    f"{total_crimes:,}"
)

col2.metric(
    "Municípios",
    total_municipios
)

col3.metric(
    "Crime Mais Frequente",
    crime_mais_comum
)

st.markdown("---")

# ==================================================
# PRIMEIRA LINHA DE GRÁFICOS
# ==================================================

col_graf1, col_graf2 = st.columns(2)

with col_graf1:

    st.subheader("Top 10 Municípios")

    top_municipios = (
        df.groupby("municipio")["registros"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        top_municipios,
        x="registros",
        y="municipio",
        orientation="h"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col_graf2:

    st.subheader("Tipos de Crime")

    tipos = (
        df.groupby("natureza")["registros"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.pie(
        tipos,
        values="registros",
        names="natureza"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==================================================
# SEGUNDA LINHA DE GRÁFICOS
# ==================================================

col_graf3, col_graf4 = st.columns(2)

with col_graf3:

    st.subheader("Crimes por Mês")

    por_mes = (
        df.groupby("mes")["registros"]
        .sum()
        .reset_index()
    )

    fig3 = px.line(
        por_mes,
        x="mes",
        y="registros",
        markers=True
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col_graf4:

    st.subheader("Crimes por RISP")

    por_risp = (
        df.groupby("risp")["registros"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        por_risp,
        x="risp",
        y="registros"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==================================================
# TABELA FINAL
# ==================================================

st.markdown("---")

st.subheader("Dados Filtrados")

st.dataframe(
    df,
    use_container_width=True
)