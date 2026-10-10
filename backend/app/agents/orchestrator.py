from app.agents.final_report import FinalReportAgent
from app.agents.document_analysis import DocumentAnalysisAgent
from app.agents.methodology import MethodologyAgent
from app.agents.research_gap import ResearchGapAgent


class ResearchOrchestrator:

    def __init__(self):
        self.document_agent = DocumentAnalysisAgent()
        self.methodology_agent = MethodologyAgent()
        self.research_gap_agent = ResearchGapAgent()
        self.final_report_agent = FinalReportAgent()

    def analyze(
        self,
        db,
        question: str,
        limit: int = 5
    ) -> dict:

        # 1. Analyze the research problem
        document_analysis = self.document_agent.analyze(
            db=db,
            question=question,
            limit=limit
        )

        # 2. Analyze the methodology
        methodology_question = (
            "What methodology, approach, models, "
            "experiments, datasets, and evaluation methods "
            "does this research paper use?"
        )

        methodology = self.methodology_agent.analyze(
            db=db,
            question=methodology_question,
            limit=limit
        )

        # 3. Analyze research gaps
        research_gap_question = (
            "What research gaps, open research questions, "
            "limitations, and future research opportunities "
            "are identified in this research paper?"
        )

        research_gaps = self.research_gap_agent.analyze(
            db=db,
            question=research_gap_question,
            limit=limit
        )
        final_report = self.final_report_agent.generate_report(
            document_analysis=document_analysis,
            methodology=methodology,
            research_gaps=research_gaps
        )

        # 4. Combine all agent outputs
        return {
            "question": question,
            "document_analysis": document_analysis,
            "methodology": methodology,
            "research_gaps": research_gaps,
            "final_report": final_report
        }