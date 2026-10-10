from app.llm.client import LLMClient


class FinalReportAgent:

    def __init__(self):
        self.llm = LLMClient()

    def generate_report(
        self,
        document_analysis: str,
        methodology: str,
        research_gaps: str
    ) -> str:

        prompt = f"""
You are the final research report agent in a multi-agent
research analysis system.

Your task is to combine the outputs of three specialized
research agents into one coherent research report.

IMPORTANT RULES:

1. Use ONLY the information provided by the three agents.
2. Do not invent facts.
3. Do not introduce information from outside the provided outputs.
4. Preserve uncertainty and limitations identified by the agents.
5. If information is missing, explicitly say that it was not
   available in the provided analysis.
6. Do not repeat the same information unnecessarily.

DOCUMENT ANALYSIS:
{document_analysis}

METHODOLOGY ANALYSIS:
{methodology}

RESEARCH GAP ANALYSIS:
{research_gaps}

Create the final report using this structure:

# Research Paper Analysis

## 1. Research Problem
Explain the main problem or area addressed by the paper.

## 2. Research Objective
Describe what the paper is trying to investigate or understand.

## 3. Methodology
Describe the research methodology, data sources,
models/frameworks, interviews, experiments, or evaluation
methods identified by the agents.

## 4. Key Approach
Explain the main conceptual or technical approach used
in the paper.

## 5. Research Gaps
Describe the important research gaps identified.

## 6. Open Research Questions
List the important unanswered questions identified by the paper.

## 7. Future Research Opportunities
Describe the future research directions identified.

## 8. Evidence
Summarize the strongest evidence supporting the analysis.

## 9. Limitations
Clearly describe limitations of the paper and limitations
of the retrieved evidence.

Keep the report factual, structured, and concise.
"""

        response = self.llm.generate(prompt)

        return response