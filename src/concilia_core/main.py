from fastapi import FastAPI

from src.concilia_core.api import health

app = FastAPI(
    title="Concilia Core",
    description="Backend para conciliação bancária",
    version="0.1.0",
)

app.include_router(health.router)
