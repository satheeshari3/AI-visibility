"""Client for OpenAI ChatGPT API."""

import os
from openai import AsyncOpenAI

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MAX_TOKENS = 500


class ChatGPTClient:
    """Handles all communication with OpenAI ChatGPT API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> None:
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key or not str(key).strip():
            raise ValueError(
                "OPENAI_API_KEY is not set. Add it to your .env file or environment."
            )
        self._client = AsyncOpenAI(api_key=key)
        self._model = model
        self._max_tokens = max_tokens

    async def complete(self, prompt: str) -> str:
        """Send a prompt to ChatGPT and return the response text.

        Args:
            prompt: The user prompt to send

        Returns:
            The assistant's response text, or empty string on error
        """
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=self._max_tokens,
            )
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                return content or ""
            return ""
        except Exception:
            return ""
