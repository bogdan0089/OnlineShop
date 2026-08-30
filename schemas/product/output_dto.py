
from pydantic import BaseModel, ConfigDict

from core.enum import ProductStatus
from schemas.category.output_dto import CategoryOutputDTO


class ProductOutputDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    color: str
    status: ProductStatus
    image_url: str | None = None
    quantity: int = 0
    description: str | None = None
    category: CategoryOutputDTO | None = None
