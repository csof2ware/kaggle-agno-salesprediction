from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AGNO AI ENGINE")

app.include_router(router)