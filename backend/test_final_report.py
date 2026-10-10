from app.agents.final_report import FinalReportAgent


document_analysis = """
The paper focuses on quantum computing and its implications
for information systems, business problems, and established
ecosystems. It uses a literature review and 21 expert interviews.
"""

methodology = """
The paper uses a literature review across EBSCO, ScienceDirect,
IEEE, and the AIS eLibrary, along with 21 interviews with
technology and academic experts. It adopts the Ding and Chong
model to distinguish hardware, system software, and application.
"""

research_gaps = """
The paper identifies unclear socio-technological consequences
of quantum computing, challenges in translating business
problems into quantum formulations, ecosystem integration
issues, and several open research questions.
"""

agent = FinalReportAgent()

result = agent.generate_report(
    document_analysis=document_analysis,
    methodology=methodology,
    research_gaps=research_gaps
)

print("\n" + "=" * 70)
print("FINAL RESEARCH REPORT")
print("=" * 70)
print(result)