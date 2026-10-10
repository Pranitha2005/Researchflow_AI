from app.db.session import SessionLocal
from app.agents.document_analysis import DocumentAnalysisAgent


question = "What problem does this research paper address?"


db = SessionLocal()

try:

    agent = DocumentAnalysisAgent()

    result = agent.analyze(
        db=db,
        question=question,
        limit=5
    )

    print("\nDOCUMENT ANALYSIS")
    print("=" * 70)
    print(result)

finally:
    db.close()