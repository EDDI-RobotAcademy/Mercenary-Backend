from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Kakao
    KAKAO_CLIENT_ID: str
    KAKAO_REDIRECT_URI: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
