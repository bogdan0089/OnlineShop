from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str | None = None
    created_at: datetime
    client_id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)

