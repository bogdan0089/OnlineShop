from pydantic import BaseModel, ConfigDict, EmailStr
from core.enum import Role


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int


class ClientUpdate(BaseModel):
    name: str
    age: int


class ResponseClient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    age: int
    balance: float


class ClientOrdersCount(BaseModel):
    client_id: int
    orders_count: int


class OperationsRequest(BaseModel):
    amount: float
