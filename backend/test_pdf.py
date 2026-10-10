from app.ingestion.pdf_parser import extract_text_from_pdf
from app.ingestion.chunker import chunk_text


PDF_PATH = "storage/sample.pdf"


pages = extract_text_from_pdf(PDF_PATH)

print("Number of pages with text:", len(pages))

for page in pages[:2]:
    print("\n--- PAGE", page["page"], "---")
    print(page["text"][:500])


chunks = chunk_text(pages)

print("\nNumber of chunks:", len(chunks))

for chunk in chunks[:3]:
    print("\n--- CHUNK", chunk["chunk_index"], "---")
    print("Page:", chunk["page"])
    print(chunk["text"][:300])