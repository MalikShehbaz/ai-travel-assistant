from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str
    database_url: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=".env")

    @model_validator(mode="after")
    def validate_postgres_password(self) -> "Settings":
        if make_url(self.database_url).password != self.postgres_password:
            raise ValueError("DATABASE_URL password must match POSTGRES_PASSWORD")
        return self


settings = Settings()
