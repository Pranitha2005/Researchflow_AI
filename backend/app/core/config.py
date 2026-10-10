
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str

    # A separate LLM key is not required for the current Gemini client.
    LLM_API_KEY: str | None = None

    LLM_MODEL: str = "gemini-3.7-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
