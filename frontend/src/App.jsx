import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useState } from "react"
import "./App.css"

const API_URL = "http://127.0.0.1:8000"

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState("")

  const handleFileChange = (event) => {
    const file = event.target.files[0]

    if (!file) return

    if (
      file.type !== "application/pdf" &&
      !file.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please select a PDF file.")
      setSelectedFile(null)
      return
    }

    setError("")
    setAnalysisResult(null)
    setSelectedFile(file)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a PDF first.")
      return
    }

    try {
      setIsAnalyzing(true)
      setError("")
      setAnalysisResult(null)

      // Step 1: Create project
      const projectName = selectedFile.name.replace(/\.pdf$/i, "")

      const projectResponse = await fetch(
        `${API_URL}/projects?name=${encodeURIComponent(
          projectName
        )}&research_question=${encodeURIComponent(
          "Analyze the research problem, methodology, research gaps, limitations, and future opportunities."
        )}`,
        { method: "POST" }
      )

      const projectData = await projectResponse.json()

      if (!projectResponse.ok) {
        throw new Error(
          projectData.detail || "Failed to create project."
        )
      }

      const projectId =
        typeof projectData === "string"
          ? projectData
          : projectData.project_id || projectData.id

      if (!projectId) {
        throw new Error("Could not find the project ID.")
      }

      // Step 2: Upload PDF
      const formData = new FormData()
      formData.append("file", selectedFile)

      const uploadResponse = await fetch(
        `${API_URL}/projects/${projectId}/documents`,
        {
          method: "POST",
          body: formData,
        }
      )

      const uploadData = await uploadResponse.json()

      if (!uploadResponse.ok) {
        throw new Error(
          uploadData.detail || "Failed to upload PDF."
        )
      }

      // Step 3: Run analysis
      const question =
        "What is the main research problem, methodology, research gaps, limitations, and future research opportunities in this paper?"

      const analysisResponse = await fetch(
        `${API_URL}/analyze?question=${encodeURIComponent(question)}`,
        { method: "POST" }
      )

      const analysisData = await analysisResponse.json()

      if (!analysisResponse.ok) {
        throw new Error(
          analysisData.detail || "Research analysis failed."
        )
      }

      setAnalysisResult(analysisData)

      // Scroll to results after React renders them
      setTimeout(() => {
        document
          .getElementById("analysis-results")
          ?.scrollIntoView({ behavior: "smooth" })
      }, 100)
    } catch (err) {
      console.error("ResearchFlow error:", err)
      setError(err.message || "Something went wrong.")
    } finally {
      setIsAnalyzing(false)
    }
  }

  const reportSections = [
    {
      title: "Research Problem",
      content: analysisResult?.document_analysis,
    },
    {
      title: "Methodology",
      content: analysisResult?.methodology,
    },
    {
      title: "Research Gaps",
      content: analysisResult?.research_gaps,
    },
  ]

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">
          ResearchFlow <span>AI</span>
        </div>
        <div className="nav-status">Research Assistant</div>
      </header>

      <main className="main-content">
        <section className="hero">
          <p className="eyebrow">AI-POWERED RESEARCH ASSISTANT</p>

          <h1>
            Understand research papers
            <br />
            <span>faster and deeper.</span>
          </h1>

          <p className="description">
            Upload a research paper and let specialized AI agents
            analyze its problem, methodology, research gaps, and
            future opportunities.
          </p>
        </section>

        <section className="upload-card">
          <div className="upload-icon">📄</div>

          <h2>Upload your research paper</h2>
          <p>PDF files are supported</p>

          <input
            type="file"
            accept=".pdf,application/pdf"
            id="pdf-upload"
            onChange={handleFileChange}
            hidden
          />

          <label htmlFor="pdf-upload" className="upload-button">
            Choose PDF
          </label>

          {selectedFile && (
            <div className="selected-file">
              <strong>Selected:</strong> {selectedFile.name}
            </div>
          )}

          <button
            className="analyze-button"
            onClick={handleUpload}
            disabled={!selectedFile || isAnalyzing}
          >
            {isAnalyzing
              ? "Analyzing Research Paper..."
              : "Upload & Analyze Paper"}
          </button>

          {isAnalyzing && (
            <p className="loading-message">
              Uploading your paper and running the AI agents.
              This may take a few minutes.
            </p>
          )}

          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}

          <p className="upload-note">
            Your paper will be analyzed by ResearchFlow AI agents.
          </p>
        </section>

        {/* Analysis Results */}
        {analysisResult && (
          <section
            className="results-section"
            id="analysis-results"
            aria-live="polite"
          >
            <div className="results-heading">
              <p className="eyebrow">ANALYSIS COMPLETE</p>
              <h2>Your Research Report</h2>
              <p>
                Results generated by your ResearchFlow AI agents.
              </p>
            </div>

            <div className="report-card final-report-card">
              <h3>📑 Final Research Report</h3>
              
<div className="report-text markdown-content">
  <ReactMarkdown remarkPlugins={[remarkGfm]}>
    {analysisResult.final_report ||
      "The final report was not returned."}
  </ReactMarkdown>
</div>

            </div>

            <h2 className="agent-results-heading">
              Individual Agent Results
            </h2>

            <div className="report-grid">
              {reportSections.map((section) => (
                <article className="report-card" key={section.title}>
                  <h3>{section.title}</h3>
                  
<div className="report-text markdown-content">
  <ReactMarkdown remarkPlugins={[remarkGfm]}>
    {section.content ||
      "No information was returned for this section."}
  </ReactMarkdown>
</div>

                </article>
              ))}
            </div>

            <button
              className="analyze-button"
              onClick={() => {
                setAnalysisResult(null)
                setError("")
                setSelectedFile(null)
              }}
            >
              Analyze Another Paper
            </button>
          </section>
        )}

        <section className="agent-section">
          <h2>What ResearchFlow analyzes</h2>

          <div className="agent-grid">
            <div className="agent-card">
              <div className="agent-number">01</div>
              <h3>Research Problem</h3>
              <p>
                Understand the main problem, objectives, and scope
                addressed by the paper.
              </p>
            </div>

            <div className="agent-card">
              <div className="agent-number">02</div>
              <h3>Methodology</h3>
              <p>
                Identify the methodology, approaches, models,
                datasets, and evaluation methods.
              </p>
            </div>

            <div className="agent-card">
              <div className="agent-number">03</div>
              <h3>Research Gaps</h3>
              <p>
                Discover open questions, limitations, and future
                research opportunities.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
