def chunk_text(
    pages: list[dict],
    chunk_size: int = 1200,
    overlap: int = 200
) -> list[dict]:
    """
    Split page text into overlapping chunks.

    Each chunk keeps its source page number.
    """

    chunks = []
    chunk_index = 0

    for page in pages:
        page_number = page["page"]
        text = page["text"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    {
                        "page": page_number,
                        "section": None,
                        "chunk_index": chunk_index,
                        "text": chunk
                    }
                )

                chunk_index += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks