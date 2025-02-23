from typing import Optional
from app.schemas.user import User, FullUserProfile

profile_infos = {
    0: {
        "short_description": "My bio description",
        "long_bio": "This is my longer bio",
    }
}

users_content = {0: {"liked_posts": [1] * 9}}


class UserService:

    def __init__(self):
        pass

    async def get_all_users_with_pagiantion(
        self, start: int, limit: int
    ) -> tuple[list[FullUserProfile], int]:
        list_of_users = []
        keys = list(profile_infos.keys())
        total = len(keys)
        for key in range(0, len(keys), 1):
            if key < start:
                continue
            curr_key = keys[key]
            user = await self.get_user_info(curr_key)
            list_of_users.append(user)
            if len(list_of_users) >= limit:
                break
        return list_of_users, total

    @staticmethod
    async def get_user_info(user_id: int = 0) -> FullUserProfile:
        # currently reading from dictionary later read from database
        profile_info = profile_infos[user_id]
        user_content = users_content[user_id]
        user = User(**user_content)
        full_user_profile = {**profile_info, **user.model_dump()}
        return FullUserProfile(**full_user_profile)

    @staticmethod
    async def create_update_user(
        full_profile_info: FullUserProfile, new_user_id: Optional[int] = None
    ) -> int:
        """
        Create user and new unique user id if not exist otherwise update user
        Placeholder implemented later to be updated with DB.
        Args:
            full_profile_info (FullUserProfile): User information saved in database
            new_user_id (Optional[int], optional): User id if exists. Defaults to None.

        Returns:
            user_id int: existing or new user id
        """
        global profile_infos
        global users_content

        if new_user_id is None:
            new_user_id = len(profile_infos)
        liked_posts = full_profile_info.liked_posts
        short_description = full_profile_info.short_description
        long_bio = full_profile_info.long_bio

        users_content[new_user_id] = {"liked_posts": liked_posts}
        profile_infos[new_user_id] = {
            "short_description": short_description,
            "long_bio": long_bio,
        }
        return new_user_id

    @staticmethod
    async def delete_user(user_id: int):
        global profile_infos
        global users_content

        del profile_infos[user_id]
        del users_content[user_id]
