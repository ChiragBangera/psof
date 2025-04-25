from app.create_app import create_application
import pytest
from models import recreate_postgres_tables


@pytest.fixture(scope="session")
def base_testing_app():
    app = create_application()
    recreate_postgres_tables
    return app


@pytest.fixture
def testing_rate_limit():
    return 50


@pytest.fixture(scope="session")
def sample_full_user_profile() -> dict:
    return dict(
        short_description="short desc",
        long_bio="def",
        username="chirag",
        liked_posts=[1, 3, 4],
    )
