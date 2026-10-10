from app.db.session import SessionLocal
from app.agents.orchestrator import ResearchOrchestrator


db = SessionLocal()

orchestrator = ResearchOrchestrator()

question = "Analyze this research paper."

result = orchestrator.analyze(
    db=db,
    question=question,
    limit=5
)

print("\n" + "=" * 70)
print("RESEARCHFLOW AI - ORCHESTRATOR RESULT")
print("=" * 70)

print("\nDOCUMENT ANALYSIS")
print("-" * 70)
print(result["document_analysis"])

print("\nMETHODOLOGY")
print("-" * 70)
print(result["methodology"])

print("\nRESEARCH GAPS")
print("-" * 70)
print(result["research_gaps"])

print("\nFINAL RESEARCH REPORT")
print("-" * 70)
print(result["final_report"])

db.close()