from pydantic import BaseModel, ConfigDict
from core.enum import ProductStatus


class ProductCreate(BaseModel):
    name: str
    price: float = 0.0
    color: str
    image_url: str | None = None
    quantity: int = 0
    description: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None


class UpdateProductStatus(BaseModel):
    status: ProductStatus
                        

class ResponseProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    color: str
    status: ProductStatus
    image_url: str | None = None
    quantity: int = 0
    description: str | None = None

class ProductGenerateDescription(BaseModel):
    product_name: str

class AiChat(BaseModel):
    message: str