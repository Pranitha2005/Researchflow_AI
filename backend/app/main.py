
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID

from fastapi import (
    FastAPI,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.agents.orchestrator import ResearchOrchestrator
from app.db.models import Project
from app.db.session import get_db
from app.ingestion.service import ingest_document


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("ResearchFlowAI")


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="ResearchFlow AI",
    description="Multi-agent research intelligence platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Root and health endpoints
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "ResearchFlow AI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Create research project
# --------------------------------------------------

@app.post("/projects")
def create_project(
    name: str,
    research_question: str | None = None,
    db: Session = Depends(get_db),
):
    logger.info("=" * 60)
    logger.info("PROJECT CREATION STARTED")
    logger.info("Project name: %s", name)

    try:
        project = Project(
            name=name,
            research_question=research_question,
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        logger.info("Project created successfully")
        logger.info("Project ID: %s", project.id)
        logger.info("=" * 60)

        return {
            "project_id": str(project.id),
            "name": project.name,
            "research_question": project.research_question,
        }

    except Exception:
        db.rollback()
        logger.exception("Project creation failed")
        raise


# --------------------------------------------------
# Upload and ingest PDF
# --------------------------------------------------

@app.post("/projects/{project_id}/documents")
async def upload_document(
    project_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    logger.info("=" * 60)
    logger.info("PDF UPLOAD STARTED")
    logger.info("Project ID: %s", project_id)

    temp_path = None

    try:
        # Step 1: Verify project
        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if not project:
            logger.warning("Project not found: %s", project_id)
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        logger.info("Project verified: %s", project.name)

        # Step 2: Validate filename and file type
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is required",
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported",
            )

        logger.info("PDF filename: %s", file.filename)

        # Step 3: Save uploaded PDF temporarily
        suffix = Path(file.filename).suffix

        with NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_path = Path(temp_file.name)

            content = await file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="The uploaded PDF is empty",
                )

            temp_file.write(content)

        logger.info(
            "PDF received successfully: %.2f KB",
            len(content) / 1024,
        )

        # Step 4: Run ingestion pipeline
        logger.info(
            "Starting PDF parsing, chunking, and embedding..."
        )

        document = ingest_document(
            db=db,
            project_id=project_id,
            source_file=temp_path,
        )

        logger.info("Document ingestion completed")
        logger.info("Document ID: %s", document.id)
        logger.info("Document status: %s", document.status)
        logger.info("PDF UPLOAD COMPLETED")
        logger.info("=" * 60)

        return {
            "message": "Document ingested successfully",
            "document_id": str(document.id),
            "filename": document.filename,
            "status": document.status,
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        logger.exception("PDF upload or ingestion failed")
        raise HTTPException(
            status_code=500,
            detail="PDF ingestion failed. Check the backend terminal logs.",
        )

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

        await file.close()


# --------------------------------------------------
# Analyze research paper
# --------------------------------------------------

@app.post("/analyze")
def analyze_research_paper(
    question: str,
    db: Session = Depends(get_db),
):
    logger.info("=" * 60)
    logger.info("RESEARCH ANALYSIS STARTED")
    logger.info("Research question: %s", question)

    try:
        orchestrator = ResearchOrchestrator()

        result = orchestrator.analyze(
            db=db,
            question=question,
            limit=5,
        )

        logger.info("Document analysis agent: completed")
        logger.info("Methodology agent: completed")
        logger.info("Research gap agent: completed")

        final_report = result.get("final_report", "")

        logger.info("Final report generated")
        logger.info(
            "Final report length: %s characters",
            len(final_report)
            if isinstance(final_report, str)
            else 0,
        )
        logger.info("RESEARCH ANALYSIS COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

        # The API response still contains the complete report.
        return result

    except Exception:
        logger.exception("RESEARCH ANALYSIS FAILED")
        raise
