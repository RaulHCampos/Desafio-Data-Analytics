import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

#- Geração do dataser simulado (ecom_data.csv com 5001 linhas)


clientes = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda"]
produtos = ["Notebook", "Mouse", "Teclado", "Monitor", "Headset"]
categorias = ["Eletrônicos", "Acessórios"]
cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba"]

dados = []

for i in range(5001):
    
    data = datetime(2024,1,1) + timedelta(days=random.randint(0,365))
    
    registro = {
        "id_pedido": i+1,
        "cliente": random.choice(clientes),
        "produto": random.choice(produtos),
        "categoria": random.choice(categorias),
        "preco": round(random.uniform(50,5000),2),
        "quantidade": random.randint(1,5),
        "data_pedido": data.strftime("%d/%m/%Y"),
        "cidade": random.choice(cidades)
    }
    
    dados.append(registro)

df = pd.DataFrame(dados)

df.to_csv("ecom_data.csv", index=False)

print("Dataset criado com sucesso!")

# - Tratamento dos dados nulos, duplicados e inconsistentes
df = df.dropna()
df = df.drop_duplicates()
# - Padronização de formatos(datas, moedas)
df["data_pedido"] = pd.to_datetime(df["data_pedido"], dayfirst=True)
df["preco"] = df["preco"].astype(float)

# - Carga dos dados tratados num banco de dados relacional.

import sqlite3

conn = sqlite3.connect("ecommerce.db")

df.to_sql("vendas", conn, if_exists="replace", index=False)
                        
conn.close()

print("Dados carregados no banco com sucesso!")