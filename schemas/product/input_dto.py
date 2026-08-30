
from pydantic import BaseModel, Field

from core.enum import ProductStatus


class ProductCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(0.0, ge=0)
    color: str = Field(..., min_length=1)
    image_url: str | None = None
    quantity: int = Field(0, ge=0)
    description: str | None = None
    category_id: int | None = None


class ProductUpdateDTO(BaseModel):
    name: str | None = Field(None, min_length=1)
    price: float | None = Field(None, ge=0)
    description: str | None = None
    quantity: int | None = Field(None, ge=0)
    category_id: int | None = None


class ProductStatusUpdateDTO(BaseModel):
    status: ProductStatus


class ProductGenerateDescriptionDTO(BaseModel):
    product_name: str = Field(..., min_length=1)


class AiChatDTO(BaseModel):
    message: str = Field(..., min_length=1)
