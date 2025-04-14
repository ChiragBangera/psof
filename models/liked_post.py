from models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    UniqueConstraint,
    ForeignKeyConstraint,
    Index,
)
from datetime import datetime, timezone


class LikedPost(Base):

    __tablename__ = "liked_post"

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="user_post_unique"),
        ForeignKeyConstraint(["user_id"], ["user.id"]),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(Integer, nullable=False)
    post_id = Column(Integer, nullable=False)


Index("liked _post_user_idx", LikedPost.user_id)
