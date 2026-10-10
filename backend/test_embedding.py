from app.embeddings.service import generate_embedding


text = """
Transformers are neural network architectures widely used
for natural language processing and research analysis.
"""

embedding = generate_embedding(text)

print("Embedding generated successfully!")
print("Dimensions:", len(embedding))
print("First 10 values:", embedding[:10])