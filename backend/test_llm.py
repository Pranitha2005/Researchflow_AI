from app.llm.client import LLMClient


llm = LLMClient()


prompt = """
You are a research assistant.

Explain in 3 simple sentences:
Why is semantic search useful when analyzing research papers?
"""


response = llm.generate(prompt)


print("\nLLM RESPONSE")
print("=" * 60)
print(response)