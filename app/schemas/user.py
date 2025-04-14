from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str = Field(
        alias="name",
        title="The username",
        description="This is the username of the user",
        min_length=1,
        max_length=20,
        default="No name",
    )
    liked_posts: Optional[list[int]] = Field(
        description="Array of post ids like by the user", default=None
    )


class FullUserProfile(User):
    short_description: str
    long_bio: str


class MultipleUsersResponse(BaseModel):
    users: list[FullUserProfile]
    total: int


class CreateUserResponse(BaseModel):
    user_id: int
