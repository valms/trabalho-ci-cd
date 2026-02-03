import os

from fastapi import FastAPI

from src.concilia_core.api import health, transactions

app = FastAPI(title="Concilia-Core", version="0.1.0")

app.include_router(health.router)
app.include_router(transactions.router)


@app.get("/version")
async def get_version():
    return {
        "version": os.getenv("APP_VERSION", "unknown"),
        "env": os.getenv("ENV_NAME", "not_set")
    }
