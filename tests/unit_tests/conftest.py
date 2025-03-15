import pytest
from app.services.user import UserService


@pytest.fixture
def _profile_infos():
    val = {
        0: {
            "short_description": "My bio description",
            "long_bio": "This is my longer bio",
        }
    }
    return val


@pytest.fixture
def _users_content():
    val = {0: {"liked_posts": [1] * 9}}
    return val


@pytest.fixture(scope="function", autouse=True)
def testing_fixture():
    print("Initializing fixture")
    return "a"


@pytest.fixture
def user_service(_profile_infos, _users_content):
    user_service = UserService(_profile_infos, _users_content)
    return user_service
