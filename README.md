# ResearchFlow AI 🔬

**An AI-powered research paper analysis platform using Retrieval-Augmented Generation (RAG) and specialized AI agents.**

ResearchFlow AI helps users analyze research papers, retrieve relevant information, and generate structured insights from uploaded PDF documents.

## 📸 Application Screenshots

### Application Interface

![ResearchFlow AI Application](screenshots/application.png)

### AI Analysis Results

![ResearchFlow AI Analysis Results](screenshots/analysis-results.png)


## ✨ Features

- **PDF Upload:** Upload research papers for analysis.
- **Document Analysis:** Generate answers using information retrieved from document content.
- **Semantic Search:** Find relevant text chunks using vector embeddings.
- **Multi-Agent Analysis:** Organize analysis into specialized areas, including document analysis, methodology analysis, and research gap analysis.
- **Automated Reports:** Combine analysis results into a structured report.
- **Markdown Rendering:** Display formatted analysis and reports in the web interface.

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- React Markdown
- remark-gfm

### Backend
- Python
- FastAPI
- SQLAlchemy
- PyMuPDF

### AI and Retrieval
- Google Gemini API
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Vector embeddings
- PostgreSQL with pgvector
- Retrieval-Augmented Generation (RAG)

## 🏗️ Project Structure

```text
Researchflow_AI/
├── backend/
│   └── app/
│       ├── agents/
│       ├── core/
│       ├── db/
│       ├── llm/
│       └── retrieval/
├── frontend/
│   └── src/
├── .gitignore
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.10 or a compatible version for the project dependencies
- Node.js and npm
- A PostgreSQL database configured with pgvector
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/Pranitha2005/Researchflow_AI.git
cd Researchflow_AI
```

### 2. Configure the backend

Open a terminal in the project root:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies using your project's dependency file, such as `requirements.txt` if present.

Create a `.env` file using the variable names required by the backend configuration. Configure your database connection and Gemini API key locally. **Never commit your `.env` file or secrets to GitHub.**

Start the backend using the project's configured FastAPI entry point. For the current setup, this may be:

```bash
uvicorn app.main:app --reload
```

The API is expected to run at `http://127.0.0.1:8000` when using the default configuration.

### 3. Configure the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, commonly `http://localhost:5173`.

## 🔍 How It Works

1. Upload a research paper in PDF format.
2. Extract text and divide it into smaller chunks.
3. Generate vector embeddings for the chunks.
4. Retrieve relevant content through semantic search.
5. Use the LLM and specialized analysis agents to generate insights.
6. Present the analysis and final report in the React interface.

## 🔐 Security

- Store API keys and database credentials in local environment variables.
- Keep `.env` files out of version control.
- Do not upload private research documents or generated data unless you have permission.

## 🚀 Future Improvements

- Document-specific retrieval and project-level isolation.
- More robust error handling and LLM rate-limit management.
- Automated evaluation of generated answers against source documents.
- Improved research-paper comparison and export options.

## 👩‍💻 Author

**Pranitha Voruganti**

[GitHub Profile](https://github.com/Pranitha2005)

---

*ResearchFlow AI — making research-paper analysis more accessible with AI.*
