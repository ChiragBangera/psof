from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Config(BaseSettings):
    host: str

    model_config = ConfigDict(env_prefix="db_")
    # class Config:
    #     env_prefix = "db_"
