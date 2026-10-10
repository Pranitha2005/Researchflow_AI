import hashlib
import shutil
from pathlib import Path

from sqlalchemy.orm import Session

from app.embeddings.processor import generate_embeddings_for_document
from app.db.models import Document, Chunk
from app.ingestion.pdf_parser import extract_text_from_pdf
from app.ingestion.chunker import chunk_text


STORAGE_DIR = Path("storage")


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024 * 1024)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def ingest_document(
    db: Session,
    project_id,
    source_file: Path
):
    # 1. Calculate hash
    file_hash = calculate_sha256(source_file)

    # 2. Check for duplicate
    existing_document = (
        db.query(Document)
        .filter(Document.sha256 == file_hash)
        .first()
    )

    if existing_document:
        return existing_document

    # 3. Copy PDF into storage
    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = STORAGE_DIR / source_file.name

    shutil.copy2(
        source_file,
        destination
    )

    # 4. Create document record
    document = Document(
        project_id=project_id,
        filename=source_file.name,
        storage_path=str(destination),
        sha256=file_hash,
        status="PROCESSING"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # 5. Extract pages
    pages = extract_text_from_pdf(
        str(destination)
    )

    # 6. Create chunks
    chunks = chunk_text(pages)

    # 7. Store chunks
    for chunk_data in chunks:
        chunk = Chunk(
            document_id=document.id,
            page=chunk_data["page"],
            section=chunk_data["section"],
            chunk_index=chunk_data["chunk_index"],
            text=chunk_data["text"]
        )

        db.add(chunk)

    # 8. Mark document as ready
    generate_embeddings_for_document(
        db=db,
        document_id=document.id
    )

    document.status = "READY"
    db.commit()

    return document