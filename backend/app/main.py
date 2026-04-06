from fastapi import FastAPI
from app.api.routes import router

from app.database.db import engine, Base
from app.database import models  # necessário para criar tabelas

app = FastAPI(title="AGNO AI ENGINE")

# cria tabelas no banco
Base.metadata.create_all(bind=engine)

# registra rotas
app.include_router(router)