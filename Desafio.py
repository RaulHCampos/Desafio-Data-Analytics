import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# SPRINT 3: Dashboard com Streamlit
# ============================================================

BASE_DIR = Path(__file__).parent

st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("📊 Dashboard — Desafio Data Analytics")

# --- Carregando os dados ---
conn = sqlite3.connect(BASE_DIR / "ecommerce.db")
df = pd.read_sql("SELECT * FROM vendas", conn)
conn.close()

df["data_pedido"] = pd.to_datetime(df["data_pedido"])
df["receita"] = df["preco"] * df["quantidade"]
df["mes"] = df["data_pedido"].dt.to_period("M").astype(str)

# ============================================================
# FILTROS DINÂMICOS (barra lateral)
# ============================================================
st.sidebar.header("🔍 Filtros")

clientes = st.sidebar.multiselect(
    "Cliente",
    options=df["cliente"].unique(),
    default=df["cliente"].unique()
)

produtos = st.sidebar.multiselect(
    "Produto",
    options=df["produto"].unique(),
    default=df["produto"].unique()
)

cidades = st.sidebar.multiselect(
    "Cidade",
    options=df["cidade"].unique(),
    default=df["cidade"].unique()
)

data_min = df["data_pedido"].min().date()
data_max = df["data_pedido"].max().date()
intervalo = st.sidebar.date_input("Período", [data_min, data_max])

# Aplicando filtros
df_filtrado = df[
    (df["cliente"].isin(clientes)) &
    (df["produto"].isin(produtos)) &
    (df["cidade"].isin(cidades)) &
    (df["data_pedido"].dt.date >= intervalo[0]) &
    (df["data_pedido"].dt.date <= intervalo[1])
]

# ============================================================
# KPIs PRINCIPAIS
# ============================================================
st.subheader("📌 KPIs Principais")

faturamento = df_filtrado["receita"].sum()
ticket_medio = df_filtrado["receita"].mean()
total_pedidos = len(df_filtrado)
clientes_ativos = df_filtrado["cliente"].nunique()

# Taxa de retenção — clientes que compraram em mais de 1 mês
compras_por_mes = df_filtrado.groupby("cliente")["mes"].nunique()
retidos = (compras_por_mes > 1).sum()
retencao = retidos / clientes_ativos * 100 if clientes_ativos > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Faturamento Total", f"R$ {faturamento:,.2f}")
col2.metric("🎫 Ticket Médio",      f"R$ {ticket_medio:,.2f}")
col3.metric("📦 Total de Pedidos",  f"{total_pedidos:,}")
col4.metric("👥 Clientes Ativos",   f"{clientes_ativos}")
col5.metric("🔄 Taxa de Retenção",  f"{retencao:.1f}%")

st.divider()

# ============================================================
# GRÁFICOS
# ============================================================
col_a, col_b = st.columns(2)

# Série temporal — faturamento mensal
with col_a:
    st.subheader("📅 Faturamento Mensal (Sazonalidade)")
    fat_mensal = df_filtrado.groupby("mes")["receita"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(fat_mensal["mes"], fat_mensal["receita"], marker="o", color="steelblue")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Receita (R$)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Receita por produto
with col_b:
    st.subheader("📦 Receita por Produto")
    fat_produto = df_filtrado.groupby("produto")["receita"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.barh(fat_produto.index, fat_produto.values, color="steelblue")
    ax.set_xlabel("Receita (R$)")
    plt.tight_layout()
    st.pyplot(fig)

col_c, col_d = st.columns(2)

# Receita por cidade
with col_c:
    st.subheader("🏙️ Receita por Cidade")
    fat_cidade = df_filtrado.groupby("cidade")["receita"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.barh(fat_cidade.index, fat_cidade.values, color="coral")
    ax.set_xlabel("Receita (R$)")
    plt.tight_layout()
    st.pyplot(fig)

# Pedidos por cliente
with col_d:
    st.subheader("👤 Pedidos por Cliente")
    pedidos_cliente = df_filtrado.groupby("cliente")["id_pedido"].count().sort_values()
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.barh(pedidos_cliente.index, pedidos_cliente.values, color="mediumseagreen")
    ax.set_xlabel("Qtd. Pedidos")
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# Tabela de dados filtrados
st.subheader("🗂️ Dados Filtrados")

st.dataframe(df_filtrado.sort_values("data_pedido", ascending=False), use_container_width=True)