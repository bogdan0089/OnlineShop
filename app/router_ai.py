from fastapi import APIRouter
from services.ai_service import AiService
from utils.dependencies import CurrentClient, CurrentAdmin
from schemas.product_schema import ProductGenerateDescription



router_ai = APIRouter(prefix="/ai")


@router_ai.get("/recommendations")
async def get_client_recommendations(current_client: CurrentClient) -> str:
    return await AiService.get_client_recommendations(current_client.id)

@router_ai.post("/generate-description")
async def product_generate_description(_: CurrentAdmin, data: ProductGenerateDescription) -> str:
    return await AiService.generate_product_description(data.product_name)