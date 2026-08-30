from decimal import Decimal

from core.enum import TransactionType
from database.unit_of_work import UnitOfWork
from schemas.transaction.input_dto import TransactionCreateDTO
from utils.logger import get_logger

logger = get_logger(__name__)


class PaymentService:

    @staticmethod
    async def handle_payment_success(client_id: int, amount: Decimal):
        async with UnitOfWork() as uow:
            client = await uow.client.get_client(client_id)
            if client:
                client.balance += amount
                await uow.transaction.create_transaction(TransactionCreateDTO(
                    amount=amount,
                    type=TransactionType.deposit,
                    description="deposit",
                    client_fk=client.id
                ))
        logger.info("payment_success", extra={"extra_fields": {"client_id": client_id, "amount": amount}})
