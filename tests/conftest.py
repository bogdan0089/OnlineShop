import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
import database.database as db_module
import database.unit_of_work as uow_module
import services.client_service as client_svc
import services.product_service as product_svc
import services.order_service as order_svc
from app.main import app


class FakeRedis:
    async def get(self, key): return None
    async def set(self, key, value, ex=None): pass
    async def keys(self, pattern): return []
    async def delete(self, *keys): pass


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    engine = create_async_engine(db_module.async_engine.url, poolclass=NullPool)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    orig = uow_module.async_session_maker
    uow_module.async_session_maker = session_maker

    fake = FakeRedis()
    client_svc.redis_client = fake
    product_svc.redis_client = fake
    order_svc.redis_client = fake

    yield
    uow_module.async_session_maker = orig


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def new_client(client):
    payload = {
        "name": "Bohdan",
        "email": f"user_{uuid.uuid4().hex[:8]}@gmail.com",
        "password": "pass123",
        "age": 25,
    }
    response = client.post("/auth/register", json=payload)
    payload["id"] = response.json()["id"]
    return payload


@pytest.fixture
def auth_headers(client, new_client):
    response = client.post("/auth/client_login", data={
        "username": new_client["email"],
        "password": new_client["password"],
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
