from fastapi import APIRouter, Depends
from schemas.review.input_dto import ReviewCreate
from schemas.review.output_dto import ReviewResponse
from services.review_service import ReviewService
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from utils.dependencies import CurrentClient


router_review = APIRouter(prefix="/review", tags=["Review"])


async def get_review_service(session: AsyncSession = Depends(get_session)) -> ReviewService:
    return ReviewService(session)

@router_review.post("/", response_model=ReviewResponse)
async def create_review(
    current_client: CurrentClient,
    data: ReviewCreate,
    service: ReviewService = Depends(get_review_service)
) -> ReviewResponse:
    return await service.create_review(data, current_client.id)

@router_review.get("/product/{product_id}", response_model=list[ReviewResponse])
async def get_review_by_product_id(product_id: int, service: ReviewService = Depends(get_review_service)) -> list[ReviewResponse]:
    return await service.get_reviews_by_product_id(product_id)

@router_review.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, service: ReviewService = Depends(get_review_service)) -> ReviewResponse:
    return await service.get_review(review_id)

@router_review.delete("/{review_id}", status_code=204)
async def review_delete(review_id: int, service: ReviewService = Depends(get_review_service)) -> None:
    await service.delete_review(review_id)