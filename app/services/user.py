from typing import Optional
from app.clients.db import DatabaseClient
from app.schemas.user import FullUserProfile
from app.exceptions import UserNotFound, UserAlreadyExist
from sqlalchemy import select, delete, update
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import Select
from sqlalchemy.dialects.postgresql import insert


class UserService:
    def __init__(self, database_client: DatabaseClient):
        self.database_client = database_client

    async def get_all_users_with_pagination(
        self, start: int, limit: int
    ) -> tuple[list[FullUserProfile], int]:
        query = self._get_user_info_query()
        users = await self.database_client.get_paginated(
            query=query, limit=limit, offset=start
        )
        total_query = select(func.count(self.database_client.user.c.id).label("total"))
        total_res = await self.database_client.get_first(query=total_query)
        total = total_res["total"]
        user_infos = []
        for user in users:
            user_info = dict(user)
            full_user_profile = FullUserProfile(**user_info)
            user_infos.append(full_user_profile)

        return user_infos, total

    async def get_user_info(self, user_id: int = 0) -> FullUserProfile:
        query = self._get_user_info_query(user_id=user_id)

        user = await self.database_client.get_first(query=query)

        if not user:
            raise UserNotFound(user_id=user_id)

        user_info = dict(user)

        return FullUserProfile(**user_info)

    async def create_user(self, full_profile_info: FullUserProfile) -> Optional[int]:
        # alternatively could create pydantic model, but will require some refactor
        # of other models to keep things clean
        data = dict(
            username=full_profile_info.username,
            short_description=full_profile_info.short_description,
            long_bio=full_profile_info.long_bio,
        )
        insert_stmt = (
            insert(self.database_client.user)
            .values([{**data}])
            .returning(self.database_client.user.c.id)
        )

        insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["username"])

        res = await self.database_client.get_first(insert_stmt)
        if not res:
            raise UserAlreadyExist

        new_user_id = res.id
        return new_user_id

    async def create_update_user(
        self, full_profile_info: FullUserProfile, user_id: int
    ) -> int:
        data_no_id = dict(
            username=full_profile_info.username,
            short_description=full_profile_info.short_description,
            long_bio=full_profile_info.long_bio,
        )

        data = {**data_no_id, "id": user_id}

        query = self._get_user_info_query(user_id=user_id)
        user = await self.database_client.get_first(query=query)

        user_conflist_stmt = select(self.database_client.user.c.username).where(
            self.database_client.user.c.username == full_profile_info.username,
            self.database_client.user.c.id != user_id,
        )

        username_conflict = await self.database_client.get_first(user_conflist_stmt)
        if username_conflict:
            raise UserAlreadyExist

        if not user:
            stmt = (
                insert(self.database_client.user)
                .values(**data)
                .returning(self.database_client.user.c.id)
            )

        else:
            stmt = (
                update(self.database_client.user)
                .where(self.database_client.user.c.id == user_id)
                .values(**data_no_id)
                .returning(self.database_client.user.c.id)
            )

        res = await self.database_client.get_first(stmt)

        return user_id

    async def delete_user(self, user_id: int):
        delete_stmt = delete(self.database_client.user).where(
            self.database_client.user.c.id == user_id
        )

        await self.database_client.execute_in_transaction(delete_stmt)

    def _get_user_info_query(self, user_id: Optional[int] = None) -> Select:
        liked_posts_query = select(
            self.database_client.liked_post.c.user_id,
            func.array_agg(self.database_client.liked_post.c.post_id).label(
                "liked_posts"
            ),
        ).group_by(self.database_client.liked_post.c.user_id)
        if user_id:
            liked_posts_query = liked_posts_query.where(
                self.database_client.liked_post.c.user_id == user_id
            )
        liked_posts_query = liked_posts_query.cte("liked_posts_query")

        query = select(
            self.database_client.user.c.short_description,
            self.database_client.user.c.long_bio,
            self.database_client.user.c.username.label("name"),
            liked_posts_query.c.liked_posts,
        ).join(
            liked_posts_query,
            self.database_client.user.c.id == liked_posts_query.c.user_id,
            isouter=True,
        )
        if user_id:
            query = query.where(self.database_client.user.c.id == user_id)

        return query
