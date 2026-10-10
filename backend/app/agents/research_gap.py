from app.llm.client import LLMClient
from app.retrieval.search import search_chunks


class ResearchGapAgent:

    def __init__(self):
        self.llm = LLMClient()

    def analyze(
        self,
        db,
        question: str,
        limit: int = 5
    ) -> str:

        # Step 1: Retrieve relevant research-gap chunks
        chunks = search_chunks(
            db=db,
            query=question,
            limit=limit
        )

        if not chunks:
            return "No relevant research-gap information was found in the document."

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

        # Step 3: Research-gap-specific prompt
        prompt = f"""
You are a research gap analysis agent.

Your task is to identify research gaps, open problems,
limitations, unanswered questions, and future research
opportunities mentioned in the research paper.

Use ONLY the retrieved evidence.

Do not invent research gaps that are not supported
by the evidence.

Distinguish between:
1. Explicit research gaps stated by the authors.
2. Open research questions mentioned by the authors.
3. Future research opportunities suggested by the authors.
4. Limitations explicitly stated in the evidence.

If the evidence is insufficient, clearly say so.

User Question:
{question}

Retrieved Evidence:
{evidence}

Provide your answer in this format:

Research Gaps:
<list the explicit research gaps>

Open Research Questions:
<list unanswered questions>

Future Research Opportunities:
<describe opportunities mentioned by the paper>

Evidence:
<important evidence from the retrieved passages>

Limitations:
<explain what cannot be determined from the retrieved evidence>
"""

        # Step 4: Ask Gemini
        response = self.llm.generate(prompt)

        return response