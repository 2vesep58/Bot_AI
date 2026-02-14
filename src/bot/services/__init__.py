"""Сервисы бота."""

from src.bot.services.amvera_llm import AmveraLLMService
from src.bot.services.text import process_text

__all__ = ["AmveraLLMService", "process_text"]
