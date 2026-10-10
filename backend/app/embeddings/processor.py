from sqlalchemy.orm import Session

from app.db.models import Chunk
from app.embeddings.service import generate_embedding


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def generate_embeddings_for_document(
    db: Session,
    document_id
) -> int:

    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_index)
        .all()
    )

    processed = 0

    for chunk in chunks:

        # Skip chunks that already have embeddings
        if chunk.embedding is not None:
            continue

        embedding = generate_embedding(
            chunk.text
        )

        chunk.embedding = embedding
        chunk.embedding_model = EMBEDDING_MODEL

        processed += 1

    db.commit()

    return processed