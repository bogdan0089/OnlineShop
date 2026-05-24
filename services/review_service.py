from schemas.review.input_dto import ReviewCreate
from schemas.review.output_dto import ReviewResponse
from core.exceptions import (
ReviewNotFoundError,
ReviewsNotFoundError,
ProductNotFound
)
from core.redis import redis_client
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.review_repository import ReviewRepository
from repositories.product_repository import ProductRepository
from utils.logger import get_logger


logger = get_logger(__name__)

_review_list_adapter = TypeAdapter(list[ReviewResponse])

class ReviewService:
    def __init__(self, session: AsyncSession):
        self._repo = ReviewRepository(session)
        self._repo_product = ProductRepository(session)

    async def create_review(self, data: ReviewCreate, client_id: int) -> ReviewResponse:
        review = await self._repo.create_review(data, client_id)
        async for key in redis_client.scan_iter("review*"):
            await redis_client.unlink(key)
        logger.info("review_created", extra={"extra_fields": {"review_id": review.id, "client_id": client_id}})
        return ReviewResponse.model_validate(review)

    async def get_review(self, review_id: int) -> ReviewResponse:
        review = await self._repo.get_review(review_id)
        if not review:
            logger.warning("review_not_found", extra={"extra_fields": {"review_id": review_id}})
            raise ReviewNotFoundError(review_id)
        return ReviewResponse.model_validate(review)

    async def get_reviews(self, limit: int, offset: int) -> list[ReviewResponse]:
        cached_key = f"reviews:limit:{limit}:offset:{offset}"
        cached = await redis_client.get(cached_key)
        if cached:
            return _review_list_adapter.validate_json(cached)
        reviews = await self._repo.get_reviews(limit, offset)
        if not reviews:
            raise ReviewsNotFoundError()
        validate = _review_list_adapter.validate_python(reviews)
        await redis_client.set(
            cached_key, _review_list_adapter.dump_json(validate),
            ex=60
        )
        return validate

    async def get_reviews_by_product_id(self, product_id: int) -> list[ReviewResponse]:
        cached_key = f"reviews:product:{product_id}"
        cached = await redis_client.get(cached_key)
        if cached:
            return _review_list_adapter.validate_json(cached)
        product = await self._repo_product.get_product(product_id)
        if not product:
            raise ProductNotFound(product_id)
        reviews_by_product = await self._repo.get_reviews_by_product_id(product.id)
        if not reviews_by_product:
            raise ReviewsNotFoundError()
        validate = _review_list_adapter.validate_python(reviews_by_product)
        await redis_client.set(
            cached_key, _review_list_adapter.dump_json(validate),
            ex=60
        )
        return validate

    async def delete_review(self, review_id: int) -> None:
        review = await self._repo.get_review(review_id)
        if not review:
            raise ReviewNotFoundError(review_id)
        await self._repo.delete_review(review)
        async for key in redis_client.scan_iter("review*"):
            await redis_client.unlink(key)
        logger.info("review_deleted", extra={"extra_fields": {"review_id": review_id}})
