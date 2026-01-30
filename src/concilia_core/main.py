from fastapi import FastAPI
from src.concilia_core.api import health

description = """
### MatchPoint - Conciliação Bancária Inteligente

API robusta projetada para automação de rotinas contábeis, focada na extração, 
processamento e match de transações financeiras.
"""

app = FastAPI(
    title="Concilia-Core",
    description=description,
    version="0.1.0",
    contact={
        "name": "Valmar Júnior",
        "url": "https://github.com/valms",
    },
)

app.include_router(health.router)
