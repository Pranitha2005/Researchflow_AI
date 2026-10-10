from sqlalchemy import text
from sqlalchemy.orm import Session

from app.embeddings.service import generate_embedding


def search_chunks(
    db: Session,
    query: str,
    limit: int = 5
):
    print("\n[SEARCH] Query:", query)

    # Generate embedding for the user's question
    query_embedding = generate_embedding(query)

    print("[SEARCH] Embedding dimensions:", len(query_embedding))

    

    count_result = db.execute(
        text("""
            SELECT COUNT(*)
            FROM chunks
            WHERE embedding IS NOT NULL
        """)
    )

    embedding_count = count_result.scalar()

    print(
        "[SEARCH] Chunks with embeddings:",
        embedding_count
    )
     # Convert embedding to pgvector format
    embedding_string = "[" + ",".join(
        str(value) for value in query_embedding
    ) + "]"

    db.execute(
        text("SET LOCAL ivfflat.probes = 10")
    )
    sql = text("""
        SELECT
            id,
            document_id,
            page,
            section,
            chunk_index,
            text,
            1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM chunks
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "embedding": embedding_string,
            "limit": limit
        }
    )

    rows = result.mappings().all()

    print("[SEARCH] Results found:", len(rows))

    for row in rows:
        print(
            "[SEARCH] Page:",
            row["page"],
            "| Similarity:",
            row["similarity"]
        )

    return [dict(row) for row in rows]