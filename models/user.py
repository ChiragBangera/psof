from models.base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, String, UniqueConstraint, func


class User(Base):
    __tablename__ = "user"

    __table_args__ = (UniqueConstraint("username", name="username_unique"),)

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    username = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    long_bio = Column(String)
