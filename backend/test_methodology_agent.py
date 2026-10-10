from app.db.session import SessionLocal
from app.agents.methodology import MethodologyAgent


db = SessionLocal()

agent = MethodologyAgent()

question = "What methodology does this research paper propose?"

result = agent.analyze(
    db=db,
    question=question,
    limit=5
)

print("\n" + "=" * 70)
print("METHODOLOGY ANALYSIS")
print("=" * 70)
print(result)

db.close()