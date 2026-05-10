from pydantic import BaseModel, Field
from typing import Optional, List


class QueryResponse(BaseModel):
    """Response model for paper queries"""
    question: str = Field(..., description="The question asked")
    simple_explanation: str = Field(..., description="Simplified explanation for BSCS students")
    technical_details: str = Field(..., description="Technical details and depth")
    methodology: str = Field(..., description="Methodology, model, dataset, pipeline")
    equations: str = Field(..., description="Step-by-step equation explanations")
    visual_architecture: str = Field(..., description="Visual/architecture description")
    key_points: List[str] = Field(default_factory=list, description="Key takeaways")
    citations: List[str] = Field(default_factory=list, description="Citations from paper")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="ok", description="API status")
    vector_db_loaded: bool = Field(default=False, description="Vector database status")


class DocumentInfo(BaseModel):
    """Information about loaded document"""
    file_id: str = Field(..., description="File ID")
    filename: str = Field(..., description="Filename")
    pages: int = Field(..., description="Number of pages")
    chunks: int = Field(..., description="Number of chunks")
    indexed: bool = Field(default=True, description="Whether document is indexed")
