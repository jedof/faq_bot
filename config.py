from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TG_TOKEN: SecretStr
    ADMIN_USER: int


settings = Settings()