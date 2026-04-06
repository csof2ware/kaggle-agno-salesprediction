# AGNO AI Kaggle Sales Prediction

Motor de inteligência de mercado com foco em tendências e produtos do Mercado Livre, integrado a backend FastAPI, persistência local e frontend React.

## Objetivo

Este projeto foi criado para:

- extrair tendências de mercado
- identificar produtos com alta demanda
- estimar faturamento
- calcular score de oportunidade
- apoiar decisões de compra e revenda
- servir como base técnica para análises no Jupyter Notebook/Kaggle

## Arquitetura

```text
Jupyter Notebook / Kaggle
        ↓
Exploração e tratamento
        ↓
FastAPI Backend
        ↓
Auth Mercado Livre + Refresh Token
        ↓
Motor de decisão
        ↓
Persistência local
        ↓
Frontend React

===============================================================================
Fluxo funcional

O backend autentica na API do Mercado Livre
Se o access token estiver expirado, renova usando refresh token
Tenta obter tendências reais
Se tendências falharem, usa fallback por keywords estratégicas
Busca produtos relacionados
Calcula score de oportunidade
Enriquece dados dos itens
Salva resultados
Expõe /market-analysis
O frontend consome e exibe catálogo + tendências


O projeto usa o fluxo OAuth do Mercado Livre com:

    authorization code
    access token
    refresh token
    
    
Variáveis necessárias

    ML_CLIENT_ID=
    ML_CLIENT_SECRET=
    ML_REDIRECT_URI=
    ML_AUTH_CODE=
    ML_ACCESS_TOKEN=
    ML_REFRESH_TOKEN=
    ML_TOKEN_EXPIRES_AT=
    DATABASE_URL=sqlite:///./test.db
    VITE_API_URL=http://localhost:8000

Como rodar o backend

    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload


Como rodar o frontend
    cd frontend
    npm install
    npm run dev
    
Endpoint principal
    GET /market-analysis

Uso com Kaggle / Jupyter
    O notebook continua como parte central do projeto para:
    exploração de dados
    análises visuais
    prototipagem de features
    publicação e visibilidade na comunidade Kaggle

A recomendação é usar o notebook como camada de exploração e o backend como camada operacional.



Estrutura do projeto


kaggle-agno-salesprediction/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── services/
│   │   └── main.py
│   ├── runtime/
│   └── venv/
├── frontend/
│   └── src/
├── cron/
├── notebook/
├── .env
├── .env.example
├── .gitignore
└── README.md