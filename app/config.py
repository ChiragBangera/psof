from pydantic_settings import BaseSettings


class Config(BaseSettings):
    host: str

    class Config:
        env_prefix = "db_"
