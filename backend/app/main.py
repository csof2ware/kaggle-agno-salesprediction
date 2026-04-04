from fastapi import FastAPI
from app.api.routes import router
from app.database.db import engine
from app.database.models import Base


Base.metadata.create_all(bind=engine

app = FastAPI(title="AGNO AI ENGINE")

app.include_router(router)