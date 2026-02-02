from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.concilia_core.service.operations import ConciliaService

router = APIRouter(prefix="/transactions", tags=["Transactions"])
service = ConciliaService()


class TransactionCreate(BaseModel):
    description: str
    amount: float


class TransactionResponse(BaseModel):
    id: int
    status: str


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(data: TransactionCreate):
    tx_id = service.save_transaction(data.description, data.amount)
    return {"id": tx_id, "status": "PENDING"}


@router.get("/{tx_id}", response_model=TransactionResponse)
async def read_transaction_status(tx_id: int):
    res_status = service.get_transaction_status(tx_id)
    if not res_status:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return {"id": tx_id, "status": res_status}
