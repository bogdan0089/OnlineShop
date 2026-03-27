from fastapi import APIRouter, Depends
from schemas.schemas import ResponseTransaction, CreateTransaction
from services.transaction_service import TransactionService
from utils.dependencies import get_current_client


router_transaction = APIRouter(prefix="/transaction")


@router_transaction.post("/create_transaction", response_model=ResponseTransaction)
async def create_transaction(transaction: CreateTransaction):
    create_transaction = await TransactionService.create_transaction(data=transaction)
    return create_transaction

@router_transaction.get("/{transaction_id}", response_model=ResponseTransaction)
async def get_transaction(transaction_id: int, current_client=Depends(get_current_client)):
    get_transaction = await TransactionService.get_transaction(transaction_id, current_client)
    return get_transaction

@router_transaction.get("/me/transactions", response_model=list[ResponseTransaction])
async def get_my_transactions(limit: int = 10, offset: int = 0, current_client=Depends(get_current_client)):
    return await TransactionService.get_my_transactions(current_client, limit, offset)

@router_transaction.get("/{client_id}/transactions", response_model=list[ResponseTransaction])
async def client_all_transactions(client_id: int, current_client=Depends(get_current_client)):
    return await TransactionService.client_all_transactions(client_id, current_client)


