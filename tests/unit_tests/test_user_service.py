from typing import cast
from unittest.mock import Mock
import pytest
from app.exceptions import UserNotFound


@pytest.mark.asyncio
async def test_delete_user_works_properly(user_service, sample_full_user_profile):
    user_id = await user_service.create_user(sample_full_user_profile)
    assert user_id is not None
    await user_service.delete_user(user_id=user_id)
    with pytest.raises(UserNotFound):
        await user_service.get_user_info(user_id=user_id)


async def test_create_user_works_properly(
    user_service_mocked_db, sample_full_user_profile, mocking_database_client
):
    user_id = await user_service_mocked_db.create_user(sample_full_user_profile)
    mocked_function = cast(Mock, mocking_database_client.get_first)

    assert mocked_function.called
    mocked_function.assert_awaited()

    
