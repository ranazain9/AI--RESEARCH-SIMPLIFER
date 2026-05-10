import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import upload, query
from app.core.pipeline import RAGPipeline
from app.core.config import settings
from app.core.logging_config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize RAG Pipeline
rag_pipeline = RAGPipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app
    Handles startup and shutdown events
    """
    logger.info(f"Starting {settings.PROJECT_NAME} API v{settings.VERSION}")
    yield
    logger.info("Shutting down API")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RAG-based API for simplifying research papers for BSCS students",
    version=settings.VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint
    
    Returns:
        Health status and service readiness
    """
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "pipeline_ready": rag_pipeline.is_ready(),
        "upload_dir": rag_pipeline.upload_dir
    }


# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(query.router, prefix="/api/query", tags=["Query"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": f"{settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "endpoints": {
            "health": "/health",
            "upload": "/api/upload",
            "query": "/api/query",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

