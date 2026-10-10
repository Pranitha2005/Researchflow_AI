
import time

from google import genai
from app.core.config import settings


class LLMClient:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate(self, prompt: str, max_retries: int = 4) -> str:
        for attempt in range(max_retries):
            try:
                print(
                    f"[LLM] Calling model {settings.LLM_MODEL} "
                    f"(attempt {attempt + 1}/{max_retries})"
                )

                interaction = self.client.interactions.create(
                    model=settings.LLM_MODEL,
                    input=prompt
                )

                output = interaction.output_text

                if not output:
                    raise RuntimeError(
                        "Gemini returned an empty text response."
                    )

                print(f"[LLM] Response received: {len(output)} characters")
                return output

            except Exception as error:
                print(f"[LLM] Request failed: {type(error).__name__}: {error}")

                if attempt == max_retries - 1:
                    print("[LLM] All retry attempts failed.")
                    raise

                wait_time = 5 * (2 ** attempt)
                print(f"[LLM] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        raise RuntimeError("LLM generation failed.")
