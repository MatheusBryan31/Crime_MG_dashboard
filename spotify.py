import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Spotify",
    layout="wide"          
)
# =============================================================
# CARREGAMENTO DOS DADOS
# =============================================================

# URL do arquivo CSV no GitHub
# URL_DADOS = "https://raw.githubusercontent.com/Demibolt007/      Spotify-Streaming-Insights-2010-2019/refs/heads/main/Spotify%20Dataset.csv"
# Comentei a parte acima no dia 22/06/26 às 5:56

# Le o CSV diretamente da internet e salva na variavel df
df = pd.read_csv("Spotify-2023.csv")

# Remove linhas onde a coluna streams esta vazia
df = df.dropna(subset=["streams"])

# Garante que streams e um numero inteiro
df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
df = df.dropna(subset=["streams"])
df["streams"] = df["streams"].astype(int)

# Garante que released_year e um numero inteiro
df["released_year"] = pd.to_numeric(df["released_year"], errors="coerce").astype("Int64")

# =============================================================
# CABECALHO DO DASHBOARD
# =============================================================
st.title("Spotify Streaming Dashboard - Músicas mais ouvidas de 2010 a 2019")
st.write("Explorando os dados de streaming do Spotify entre 2010 e 2019")
st.markdown("---")
st.dataframe(df, use_container_width=True)

# =============================================================
# KPIs - INDICADORES NUMERICOS EM DESTAQUE
# Mostramos 3 numeros importantes no topo do dashboard
# st.metric() e a forma mais simples de mostrar um KPI no Streamlit
# =============================================================
st.subheader("Indicadores Gerais")
# divide a linha em 3 colunas iguais
col1, col2, col3 = st.columns(3)   

# KPI 1: Total de streams
total_streams = df["streams"].sum()
col1.metric("Total de streams", f"{total_streams / 1_000_000_000:.1f}B")

# KPI 2: Numero de musicas unicas
total_musicas = df["track_name"].nunique()
col2.metric("Musicas Unicas", f"{total_musicas:,}")

# KPI 3: Media de BPM (batidas por minuto)
media_bpm = df["Bpm"].mean()
col3.metric("BPM Medio", f"{media_bpm:.0f}")

st.markdown("---")


# =============================================================
# GRAFICOS
# =============================================================

# --- GRAFICO 1 e 2: primeira linha ---
col_graf1, col_graf2 = st.columns(2)

# GRAFICO 1: streams por ano (linha do tempo)
# Tipo: grafico de linha -> bom para mostrar tendencia ao longo do tempo
with col_graf1:
    st.subheader("streams por Ano")

    # Agrupa os dados somando streams por ano
    streams_por_ano = (
        df.groupby("released_year")["streams"]
        .sum()
        .reset_index()
    )
    # markers = True (mostra pontinhos em cada ano)
    fig1 = px.line(
        streams_por_ano,
        x="released_year",
        y="streams",
        markers=True        
    )
    st.plotly_chart(fig1, use_container_width=True)

# GRAFICO 2: Top 10 Artist_namea com mais streams
# Tipo: grafico de barras horizontal -> bom para comparar categorias
with col_graf2:
    st.subheader("Top 10 Artist_name por streams")
    #ascending = True (# crescente para o grafico horizontal ficar certo)
    top_Artist_name = (
        df.groupby("Artist_name")["streams"]
        .sum()
        .sort_values(ascending=True)    
        .tail(10)
        .reset_index()
    )
    # orientation = "h" (grafico de barras horizontal)
    fig2 = px.bar(
        top_Artist_name,
        x="streams",
        y="Artist_name",
        orientation="h",
        text_auto=".2s"    
    )
    st.plotly_chart(fig2, use_container_width=True)


# --- GRAFICO 3 e 4: segunda linha ---
col_graf3, col_graf4 = st.columns(2)

# GRAFICO 3: Distribuicao de generos musicais
# Tipo: grafico de pizza -> bom para mostrar proporcao entre categorias
with col_graf3:
    st.subheader("Top 10 Músicas Mais Ouvidas")

    top_musicas = (
        df.sort_values(
            "streams",
            ascending=False
        )
        .head(10)
    )

    fig3 = px.bar(
        top_musicas,
        x="streams",
        y="track_name",
        orientation="h"
    )

    st.plotly_chart(fig3, use_container_width=True)

    #Comentando o código de Suzana. O código acima eu reaproveitei.
""" with col_graf3:
    st.subheader("streams por Genero Musical")
    #head(8) para mostrar apenas os 8 generos mais populares, o resto fica em "outros"
    streams_por_genero = (
        df.groupby("Genre")["streams"]
        .sum()
        .sort_values(ascending=False)
        .head(8)           
        .reset_index()
    )

    fig3 = px.pie(
        streams_por_genero,
        values="streams",
        names="Genre"
    )
    st.plotly_chart(fig3, use_container_width=True) """
    ##BRYAN##

# GRAFICO 4: Relacao entre Danceability e streams
# Tipo: grafico de dispersao (scatter) -> bom para ver correlacao entre dois numeros
with col_graf4:
    st.subheader("Danceability vs. streams")
    #df.sample(500) para pegar apenas 500 pontos aleatorios, assim o grafico nao fica muito pesado
    #Hover_data ao passar o mouse, mostra musica e Artist_name
    fig4 = px.scatter(
        df.sample(500),   
        x="Danceability",
        y="streams",
        color="Genre",
        hover_data=["track_name", "Artist_name"]   
    )
    st.plotly_chart(fig4, use_container_width=True)


# --- GRAFICO 5 e 6: terceira linha ---
col_graf5, col_graf6 = st.columns(2)

# GRAFICO 5: Distribuicao de BPM (histograma)
# Tipo: histograma -> bom para ver como os valores se distribuem
with col_graf5:
    st.subheader("Distribuicao de BPM")
    #nbins = 30 (divide o eixo x em 30 "caixinhas" para contar quantas musicas tem em cada faixa de BPM)
    fig5 = px.histogram(
        df,
        x="Bpm",
        nbins=30           
    )
    st.plotly_chart(fig5, use_container_width=True)

# GRAFICO 6: Energy vs Valence (humor da musica)
# Tipo: scatter com tamanho variavel -> mostra tres dimensoes ao mesmo tempo
with col_graf6:
    st.subheader("Energia vs. Positividade (Valence)")
    # tamanho do ponto = quantidade de streams
    fig6 = px.scatter(
        df.sample(500),
        x="Energy",
        y="Valence",
        size="streams",   
        color="released_year",
        hover_data=["track_name", "Artist_name"]
    )
    st.plotly_chart(fig6, use_container_width=True)


# =============================================================
# TABELA DE DADOS
# Mostra as 10 musicas com mais streams
# =============================================================
st.markdown("---")
st.subheader("Top 10 Musicas por streams")

top_musicas = (
    df[["track_name", "Artist_name", "Genre", "released_year", "streams", "Popularity"]]
    .sort_values("streams", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# Faz o indice comecar em 1 ao inves de 0
top_musicas.index = top_musicas.index + 1

st.dataframe(top_musicas, use_container_width=True)