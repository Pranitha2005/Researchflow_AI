from app.llm.client import LLMClient
from app.retrieval.search import search_chunks


class DocumentAnalysisAgent:

    def __init__(self):
        self.llm = LLMClient()

    def analyze(
        self,
        db,
        question: str,
        limit: int = 5
    ) -> str:

        # Step 1: Retrieve relevant chunks
        chunks = search_chunks(
            db=db,
            query=question,
            limit=limit
        )

        if not chunks:
            return "No relevant information was found in the document."

        # Step 2: Build evidence
        evidence_parts = []

        for index, chunk in enumerate(chunks, start=1):

            evidence_parts.append(
                f"""
SOURCE {index}
Page: {chunk['page']}
Similarity: {chunk['similarity']}

{chunk['text']}
"""
            )

        evidence = "\n".join(evidence_parts)

        # Step 3: Create the LLM prompt
        prompt = f"""
You are a research paper analysis agent.

Answer the user's question using ONLY the evidence
retrieved from the research paper.

Do not invent information.

If the evidence is insufficient, clearly say so.

User Question:
{question}

Retrieved Evidence:
{evidence}

Provide your answer in this format:

Answer:
<direct answer>

Evidence:
<important evidence from the retrieved passages>

Reasoning:
<explain how the evidence supports the answer>

Limitations:
<mention if the retrieved evidence is insufficient>
"""

        # Step 4: Ask the LLM
        response = self.llm.generate(prompt)

        return response