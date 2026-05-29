from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = Field(default="development", alias="APP_ENV")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    backend_url: str = Field(default="http://localhost:8000", alias="BACKEND_URL")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")
    jwt_secret: str = Field(alias="JWT_SECRET")
    encryption_key: str = Field(alias="ENCRYPTION_KEY")
    plaid_client_id: str = Field(default="", alias="PLAID_CLIENT_ID")
    plaid_secret: str = Field(default="", alias="PLAID_SECRET")
    plaid_env: str = Field(default="sandbox", alias="PLAID_ENV")
    splitwise_consumer_key: str = Field(default="", alias="SPLITWISE_CONSUMER_KEY")
    splitwise_consumer_secret: str = Field(default="", alias="SPLITWISE_CONSUMER_SECRET")


settings = Settings()
