from fastapi import WebSocket, APIRouter
from utils.connection_manager import connection
from services.auth_service import AuthService
from database.unit_of_work import UnitOfWork
from core.enum import Role

router_websocket = APIRouter()


@router_websocket.websocket("/ws/admin")
async def websocket_endpoint(websocket: WebSocket, token: str):
    client_id = AuthService.decode_token(token)
    async with UnitOfWork() as uow:
        client = await uow.client.get_client(client_id)
        if not client:
            await websocket.close()
            return 
        if client.role != Role.superadmin:
            await websocket.close()
            return 
    await connection.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connection.disconnect(websocket)