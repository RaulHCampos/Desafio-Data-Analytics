# Desafio Data Analytics

Projeto completo de análise de dados de um e-commerce fictício, desenvolvido em 4 sprints.

## Tecnologias

- Python, Pandas, NumPy
- SQLite, SQL
- Matplotlib, Seaborn, Streamlit
- Scikit-learn

## Estrutura

```
desafio-data-analytics/
├── data/
│   ├── ecom_data.csv
│   └── ecommerce.db
├── outputs/
│   ├── sprint2_graficos.png
│   └── sprint4_previsao.png
├── sprint1_etl.py
├── sprint2_eda_sql.py
├── sprint3_dashboard.py
├── sprint4_modelo.py
├── storytelling.md
├── requirements.txt
└── README.md
```

## Sprints

**Sprint 1 — ETL**
Geração do dataset, limpeza de dados e carga no banco SQLite.

**Sprint 2 — EDA e SQL**
Estatísticas descritivas, consultas SQL (GROUP BY, Window Functions, JOIN), análise de outliers, correlação e segmentação RFM.

**Sprint 3 — Dashboard**
Dashboard interativo com Streamlit, KPIs principais e filtros dinâmicos.

**Sprint 4 — Modelo Preditivo**
Regressão linear para previsão de receita mensal com avaliação por MAE e R².

## Como rodar

**1. Clonar o repositório:**
```bash
git clone https://github.com/seu-usuario/desafio-data-analytics.git
cd desafio-data-analytics
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

**4. Executar os scripts em ordem:**
```bash
python sprint1_etl.py
python sprint2_eda_sql.py
python sprint4_modelo.py
```

**5. Rodar o dashboard:**
```bash
streamlit run sprint3_dashboard.py
```

## Documentação

Veja [storytelling.md](storytelling.md) para os insights detalhados de cada sprint.