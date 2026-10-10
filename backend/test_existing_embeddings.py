from app.db.session import SessionLocal
from app.embeddings.processor import generate_embeddings_for_document


DOCUMENT_ID = "e5196404-ba31-47c5-aaaf-461cfcd4699a"


db = SessionLocal()

try:
    count = generate_embeddings_for_document(
        db=db,
        document_id=DOCUMENT_ID
    )

    print("Embeddings generated successfully!")
    print("Chunks processed:", count)

finally:
    db.close()