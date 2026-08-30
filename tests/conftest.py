import uuid

import psycopg2
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

import database.database as db_module
import database.unit_of_work as uow_module
import services.auth_service as auth_svc
import services.category_service as category_svc
import services.client_service as client_svc
import services.order_service as order_svc
import services.product_service as product_svc
import services.review_service as review_svc
from app.main import app
from core.config import settings

TEST_DB_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
TEST_DB_SYNC_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)


class RecordingTask:
    """Stands in for a Celery task: records the call instead of reaching a broker."""

    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def delay(self, *args, **kwargs) -> None:
        self.calls.append((args, kwargs))


class FakeRedis:
    async def get(self, key): return None
    async def set(self, key, value, ex=None): pass
    async def keys(self, pattern): return []
    async def delete(self, *keys): pass
    async def incr(self, key): return 1
    async def expire(self, key, seconds): pass
    async def scan_iter(self, pattern):
        return
        yield


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    orig = uow_module.async_session_maker
    orig_db = db_module.async_session_maker
    uow_module.async_session_maker = session_maker
    db_module.async_session_maker = session_maker

    fake = FakeRedis()
    client_svc.redis_client = fake
    product_svc.redis_client = fake
    order_svc.redis_client = fake
    auth_svc.redis_client = fake
    category_svc.redis_client = fake
    review_svc.redis_client = fake

    import utils.cache as cache_module
    import utils.dependencies as deps_module
    deps_module.redis_client = fake
    cache_module.redis_client = fake

    # Without this every checkout would open a real AMQP connection: the suite
    # hangs on retries when no broker is running, and sends real email when one is.
    order_svc.send_order_status_email = RecordingTask()
    order_svc.send_new_order_notification = RecordingTask()
    auth_svc.send_verification_email = RecordingTask()
    auth_svc.send_reset_password_email = RecordingTask()

    yield
    uow_module.async_session_maker = orig
    db_module.async_session_maker = orig_db


@pytest.fixture
def client():
    return TestClient(app)


def _db_execute(sql, params):
    conn = psycopg2.connect(TEST_DB_SYNC_URL)
    conn.cursor().execute(sql, params)
    conn.commit()
    conn.close()


@pytest.fixture
def new_client(client):
    payload = {
        "name": "Bohdan",
        "email": f"user_{uuid.uuid4().hex[:8]}@gmail.com",
        "password": "pass1234",
        "age": 25,
    }
    client.post("/auth/register", json=payload)
    _db_execute("UPDATE clients SET is_verified=true WHERE email=%s", (payload["email"],))
    return payload


@pytest.fixture
def auth_headers(client, new_client):
    response = client.post("/auth/client_login", data={
        "username": new_client["email"],
        "password": new_client["password"],
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
