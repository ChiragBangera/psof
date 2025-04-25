import pytest
from app.services.user import UserService
from app.config import Config
from app.clients.db import DatabaseClient
from models.base import recreate_postgres_tables
import pytest_asyncio
from app.schemas.user import FullUserProfile
from unittest.mock import AsyncMock
from models import User, LikedPost


@pytest.fixture(scope="session")
def sample_full_user_profile() -> FullUserProfile:
    return FullUserProfile(
        short_description="short desc",
        long_bio="def",
        username="chirag",
        liked_posts=[1, 3, 4],
    )


@pytest.fixture(scope="function", autouse=True)
def testing_fixture():
    print("Initializing fixture")
    return "a"


@pytest.fixture(scope="session")
def testing_config() -> Config:
    return Config()


@pytest_asyncio.fixture
async def testing_db_client(testing_config) -> DatabaseClient:
    recreate_postgres_tables()
    database_client = DatabaseClient(testing_config, ["user", "liked_post"])
    await database_client.connect()
    yield database_client
    await database_client.disconnect()


@pytest.fixture
def user_service(testing_db_client):
    user_service = UserService(testing_db_client)
    return user_service


@pytest.fixture
def mocking_database_client() -> DatabaseClient:
    mock = AsyncMock()
    mock.user = User.__table__
    mock.liked_post = LikedPost.__table__
    return mock


@pytest.fixture
async def user_service_mocked_db(
    mocking_database_client: DatabaseClient,
) -> UserService:
    user_service = UserService(mocking_database_client)
    return user_service


