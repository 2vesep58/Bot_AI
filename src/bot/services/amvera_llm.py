"""Сервис для работы с Amvera LLM."""

import asyncio
import logging
import ssl
from typing import Optional

import aiohttp

from src.bot.config import Config


class AmveraLLMService:
    """Сервис для работы с Amvera LLM."""

    AMVERA_LLM_URL = "https://kong-proxy.yc.amvera.ru/api/v1/models/gpt"
    MODEL = "gpt-5"

    def __init__(self, config: Config):
        """
        Инициализация сервиса.

        :param config: Конфигурация бота.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def get_response(self, user_message: str) -> Optional[str]:
        """
        Получить ответ от Amvera LLM.

        :param user_message: Сообщение пользователя.
        :return: Ответ от LLM или None в случае ошибки.
        """
        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": f"Bearer {self.config.amvera.token.get_secret_value()}"
        }

        # Отключаем проверку SSL-сертификата (только для тестирования!)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        try:
            self.logger.info(f"Отправка запроса к Amvera LLM: URL={self.AMVERA_LLM_URL}, Model={self.MODEL}")
            self.logger.debug(f"Payload: {payload}")
            self.logger.debug(f"Headers: {headers}")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.AMVERA_LLM_URL,
                    json=payload,
                    headers=headers,
                    ssl=ssl_context,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    self.logger.info(f"Статус ответа от Amvera LLM: {response.status}")

                    if response.status == 200:
                        result = await response.json()
                        self.logger.info(f"Успешный ответ от Amvera LLM: {result}")
                        # Проверяем разные форматы ответа
                        if "choices" in result:
                            content = result["choices"][0]["message"]["content"]
                            self.logger.info(f"Извлеченный контент: {content}")
                            return content
                        elif "result" in result:
                            return result["result"]
                        elif "text" in result:
                            return result["text"]
                        else:
                            self.logger.error(f"Неожиданный формат ответа: {result}")
                            return None
                    else:
                        error_text = await response.text()
                        self.logger.error(
                            f"Ошибка от Amvera LLM: {response.status} - {error_text}"
                        )
                        return None
        except asyncio.TimeoutError:
            self.logger.error("Timeout при обращении к Amvera LLM")
            return None
        except Exception as e:
            self.logger.error(f"Исключение при обращении к Amvera LLM: {type(e).__name__}: {e}", exc_info=True)
            return None
