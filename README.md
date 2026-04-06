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


CURLs  fluxo Oauth Mercado Livre

O fluxo oficial do Mercado Livre usa authorization code para obter token,
 POST /oauth/token para trocar o code por token, e o access_token deve ser enviado
no header Authorization: Bearer .... 
O access_token expira em cerca de 6 horas e o refresh_token é de uso único, 
sendo necessário guardar sempre o último retornado. �

Mercado Livre Developers

1. URL de autorização no navegador
Esse passo é no browser, não no curl:

https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=SEU_APP_ID&redirect_uri=SUA_REDIRECT_URI

Depois do login/consentimento, você recebe algo como:

https://sua-redirect-uri?code=SEU_AUTH_CODE
O redirect_uri precisa bater exatamente com o configurado no app. 


2. Trocar code por access_token

curl -X POST "https://api.mercadolibre.com/oauth/token" \
  -H "accept: application/json" \
  -H "content-type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=SEU_APP_ID" \
  -d "client_secret=SEU_CLIENT_SECRET" \
  -d "code=SEU_AUTH_CODE" \
  -d "redirect_uri=SUA_REDIRECT_URI"

3. Renovar token com refresh_token

curl -X POST "https://api.mercadolibre.com/oauth/token" \
  -H "accept: application/json" \
  -H "content-type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=SEU_APP_ID" \
  -d "client_secret=SEU_CLIENT_SECRET" \
  -d "refresh_token=SEU_REFRESH_TOKEN"

Guarde o novo refresh_token retornado. O Mercado Livre informa que só o último é válido e ele é de uso único. �


4. Teste simples de autenticação

curl -X GET "https://api.mercadolibre.com/users/me" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "accept: application/json"

Esse padrão de enviar o token no header é o recomendado na documentação oficial.


5. Endpoint que estamos usando no projeto: busca por keyword

curl -X GET "https://api.mercadolibre.com/sites/MLB/search?q=ferramentas" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "accept: application/json"
6. Detalhe do item

curl -X GET "https://api.mercadolibre.com/items/ITEM_ID_AQUI" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "accept: application/json"

7. Trends do Mercado Livre, quando disponíveis no seu fluxo

curl -X GET "https://api.mercadolibre.com/trends/MLB" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "accept: application/json"

Essa rota está falhando e por isso implementamos o fallback, na proxima evolucao vamos substituir a logica com AGNO Agent.