import fitz


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
        [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]
    """

    pages = []

    document = fitz.open(file_path)

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            text = text.strip()

            if text:
                pages.append(
                    {
                        "page": page_number,
                        "text": text
                    }
                )

    finally:
        document.close()

    return pages