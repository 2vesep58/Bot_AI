from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseModel):
    """Конфигурация бота."""

    token: SecretStr


class AmveraConfig(BaseModel):
    """Конфигурация Amvera LLM."""

    token: SecretStr


class Config(BaseSettings):
    """Конфигурация приложения."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    bot_token: SecretStr
    amvera_llm_token: SecretStr

    @property
    def bot(self) -> BotConfig:
        """Конфигурация бота."""
        return BotConfig(token=self.bot_token)

    @property
    def amvera(self) -> AmveraConfig:
        """Конфигурация Amvera LLM."""
        return AmveraConfig(token=self.amvera_llm_token)


def load_config() -> Config:
    """Загрузка конфигурации."""
    return Config()