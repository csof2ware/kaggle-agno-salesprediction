from fastapi import FastAPI
from app.api.routes import router

from app.database.db import engine
from app.database.models import Base

app = FastAPI(title="AGNO AI ENGINE")

# cria tabelas no banco
Base.metadata.create_all(bind=engine)

# rotas
app.include_router(router)