from google import genai
from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Say hello to ResearchFlow AI in one sentence."
)


print("Gemini connection successful!")
print(response.output_text)