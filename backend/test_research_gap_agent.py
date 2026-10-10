from app.db.session import SessionLocal
from app.agents.research_gap import ResearchGapAgent


db = SessionLocal()

agent = ResearchGapAgent()

question = "What are the research gaps and future research opportunities identified in this paper?"

result = agent.analyze(
    db=db,
    question=question,
    limit=5
)

print("\n" + "=" * 70)
print("RESEARCH GAP ANALYSIS")
print("=" * 70)
print(result)

db.close()