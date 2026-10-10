from app.db.session import SessionLocal
from app.retrieval.search import search_chunks


queries = [
    "What is quantum computing?",
    "What are the applications of quantum computing?",
    "What are the limitations of quantum computing?",
]


db = SessionLocal()

try:
    for query in queries:

        print("\n")
        print("=" * 70)
        print("QUERY:")
        print(query)
        print("=" * 70)

        print("Generating search...")

        results = search_chunks(
            db=db,
            query=query,
            limit=5
        )

        print("Search completed!")
        print("Number of results:", len(results))

        if not results:
            print("NO RESULTS FOUND")
            continue

        for index, result in enumerate(results, start=1):

            print("\n" + "-" * 70)
            print(f"RESULT {index}")
            print("-" * 70)

            print("Page:", result["page"])
            print("Chunk:", result["chunk_index"])
            print("Similarity:", result["similarity"])

            print("\nText:")
            print(result["text"][:500])

finally:
    db.close()

print("\n")
print("=" * 70)
print("ALL QUERIES COMPLETED")
print("=" * 70)