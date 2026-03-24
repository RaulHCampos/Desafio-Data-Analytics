import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# SPRINT 2: Análise Exploratória (EDA) e SQL
# ============================================================

# Carregando os dados do banco criado no Sprint 1
conn = sqlite3.connect("ecommerce.db")
df = pd.read_sql("SELECT * FROM vendas", conn)
df["data_pedido"] = pd.to_datetime(df["data_pedido"])
df["receita"] = df["preco"] * df["quantidade"]

print("Dados carregados com sucesso!")
print(f"Total de linhas: {len(df)}\n")


# ============================================================
# 1. ESTATÍSTICAS DESCRITIVAS
# ============================================================
print("=" * 50)
print("1. ESTATÍSTICAS DESCRITIVAS")
print("=" * 50)

print(df[["preco", "quantidade", "receita"]].describe().round(2))

print(f"\nReceita total: R$ {df['receita'].sum():,.2f}")
print(f"Ticket médio: R$ {df['receita'].mean():,.2f}")


# ============================================================
# 2. CONSULTAS SQL COMPLEXAS
# ============================================================
print("\n" + "=" * 50)
print("2. CONSULTAS SQL")
print("=" * 50)

# GROUP BY — receita por produto
print("\n[GROUP BY] Receita por produto:")
q1 = """
    SELECT produto,
           COUNT(*) AS total_pedidos,
           ROUND(SUM(preco * quantidade), 2) AS receita_total
    FROM vendas
    GROUP BY produto
    ORDER BY receita_total DESC
"""
print(pd.read_sql(q1, conn).to_string(index=False))

# WINDOW FUNCTION — ranking de clientes
print("\n[WINDOW FUNCTION] Ranking de clientes por receita:")
q2 = """
    SELECT cliente,
           ROUND(SUM(preco * quantidade), 2) AS receita_total,
           RANK() OVER (ORDER BY SUM(preco * quantidade) DESC) AS ranking
    FROM vendas
    GROUP BY cliente
"""
print(pd.read_sql(q2, conn).to_string(index=False))

# JOIN com subquery — ticket por cidade vs média geral
print("\n[JOIN] Ticket médio por cidade vs. média geral:")
q3 = """
    SELECT v.cidade,
           ROUND(AVG(v.preco * v.quantidade), 2) AS ticket_cidade,
           ROUND(media.ticket_geral, 2)           AS ticket_geral
    FROM vendas v
    JOIN (SELECT AVG(preco * quantidade) AS ticket_geral FROM vendas) AS media
    GROUP BY v.cidade
    ORDER BY ticket_cidade DESC
"""
print(pd.read_sql(q3, conn).to_string(index=False))

conn.close()


# ============================================================
# 3. OUTLIERS E CORRELAÇÃO
# ============================================================
print("\n" + "=" * 50)
print("3. OUTLIERS E CORRELAÇÃO")
print("=" * 50)

# Outliers pelo método IQR
Q1 = df["receita"].quantile(0.25)
Q3 = df["receita"].quantile(0.75)
IQR = Q3 - Q1
lim_sup = Q3 + 1.5 * IQR

outliers = df[df["receita"] > lim_sup]
print(f"\nOutliers encontrados (IQR): {len(outliers)}")
print(f"Limite superior: R$ {lim_sup:,.2f}")

# Correlação
print("\nCorrelação entre variáveis:")
print(df[["preco", "quantidade", "receita"]].corr().round(3))


# ============================================================
# 4. SEGMENTAÇÃO RFM
# ============================================================
print("\n" + "=" * 50)
print("4. SEGMENTAÇÃO RFM")
print("=" * 50)

data_ref = df["data_pedido"].max() + pd.Timedelta(days=1)

rfm = df.groupby("cliente").agg(
    Recencia   = ("data_pedido", lambda x: (data_ref - x.max()).days),
    Frequencia = ("id_pedido",   "count"),
    Monetario  = ("receita",     "sum")
).reset_index()

# Score de 1 a 3 para cada métrica
rfm["R"] = pd.cut(rfm["Recencia"],   bins=3, labels=[3, 2, 1]).astype(int)
rfm["F"] = pd.cut(rfm["Frequencia"], bins=3, labels=[1, 2, 3]).astype(int)
rfm["M"] = pd.cut(rfm["Monetario"],  bins=3, labels=[1, 2, 3]).astype(int)
rfm["Score"] = rfm["R"] + rfm["F"] + rfm["M"]

def segmento(score):
    if score >= 8:
        return "Campeão"
    elif score >= 6:
        return "Leal"
    elif score >= 4:
        return "Em risco"
    else:
        return "Inativo"

rfm["Segmento"] = rfm["Score"].apply(segmento)

print(rfm[["cliente", "Recencia", "Frequencia", "Monetario", "Score", "Segmento"]]
      .sort_values("Score", ascending=False).to_string(index=False))


# ============================================================
# 5. GRÁFICOS
# ============================================================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sprint 2 — EDA", fontsize=14, fontweight="bold")

# Receita por produto
receita_produto = df.groupby("produto")["receita"].sum().sort_values()
axs[0, 0].barh(receita_produto.index, receita_produto.values)
axs[0, 0].set_title("Receita por Produto")
axs[0, 0].set_xlabel("Receita (R$)")

# Boxplot para ver outliers
axs[0, 1].boxplot(df["receita"])
axs[0, 1].set_title("Distribuição da Receita (Outliers)")
axs[0, 1].set_ylabel("Receita (R$)")

# Heatmap de correlação
sns.heatmap(df[["preco", "quantidade", "receita"]].corr(),
            annot=True, fmt=".2f", cmap="coolwarm", ax=axs[1, 0])
axs[1, 0].set_title("Correlação entre Variáveis")

# Segmentação RFM
rfm["Segmento"].value_counts().plot(kind="bar", ax=axs[1, 1], color="steelblue")
axs[1, 1].set_title("Segmentação RFM")
axs[1, 1].set_xlabel("Segmento")
axs[1, 1].set_ylabel("Qtd. Clientes")
axs[1, 1].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("sprint2_graficos.png", dpi=150)
plt.show()
print("\nGráficos salvos em sprint2_graficos.png")

print("\nSprint 2 concluído!")