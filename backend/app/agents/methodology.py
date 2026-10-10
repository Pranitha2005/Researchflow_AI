from app.llm.client import LLMClient
from app.retrieval.search import search_chunks


class MethodologyAgent:

    def __init__(self):
        self.llm = LLMClient()

    def analyze(
        self,
        db,
        question: str,
        limit: int = 5
    ) -> str:

        # Step 1: Retrieve relevant methodology-related chunks
        chunks = search_chunks(
            db=db,
            query=question,
            limit=limit
        )

        if not chunks:
            return "No relevant methodology information was found in the document."

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

        # Step 3: Create methodology-specific prompt
        prompt = f"""
You are a research paper methodology analysis agent.

Your task is to identify and explain the methodology used
in the research paper.

Answer the user's question using ONLY the retrieved evidence.

Do not invent information.

If the evidence is insufficient, clearly say so.

User Question:
{question}

Retrieved Evidence:
{evidence}

Analyze the methodology and provide your answer in this format:

Methodology:
<describe the methodology used in the paper>

Approach:
<explain the main approach, framework, algorithm, model,
or process described in the evidence>

Data / Experimental Setup:
<describe datasets, experiments, simulations, or evaluation
methods if mentioned>

Evidence:
<important evidence from the retrieved passages>

Limitations:
<mention what methodology information is missing or unclear>
"""

        # Step 4: Ask Gemini
        response = self.llm.generate(prompt)

        return response