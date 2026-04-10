# Desafio Data Analytics

Projeto completo de análise de dados de um e-commerce fictício, desenvolvido em 4 sprints.

## Tecnologias

- Python, Pandas, NumPy
- SQLite, SQL
- Matplotlib, Seaborn, Streamlit
- Scikit-learn

## Estrutura

```
Desafio Data Analytics/
├── Desafio.py
├── storytelling.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Sprints

**Sprint 1 — ETL**
Geração do dataset com 5.001 pedidos, limpeza de dados e carga no banco SQLite.

**Sprint 2 — EDA e SQL**
Estatísticas descritivas, consultas SQL (GROUP BY, Window Functions, JOIN), análise de outliers, correlação e segmentação RFM.

**Sprint 3 — Dashboard**
Dashboard interativo com Streamlit, KPIs principais (faturamento, ticket médio, taxa de retenção) e filtros dinâmicos por cliente, produto, cidade e período.

**Sprint 4 — Modelo Preditivo**
Regressão linear para previsão de receita mensal com avaliação por MAE e R², integrado ao dashboard.

## Como rodar

**1. Clonar o repositório:**
```bash
git clone https://github.com/RaulHCampos/Desafio-Data-Analytics.git
cd Desafio-Data-Analytics
```

**2. Criar e ativar a venv:**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Instalar dependências:**
```bash
pip install -r requirements.txt
```

**4. Rodar o dashboard:**
```bash
streamlit run Desafio.py
```

## Documentação

Veja [storytelling.md](storytelling.md) para os insights detalhados de cada sprint.