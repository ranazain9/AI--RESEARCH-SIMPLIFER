from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request model for querying a paper"""
    question: str = Field(..., description="Question about the research paper")
    file_id: Optional[str] = Field(None, description="File ID of uploaded PDF")


class UploadResponse(BaseModel):
    """Response model for file upload"""
    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    pages: int = Field(..., description="Number of pages in PDF")
    chunks: int = Field(..., description="Number of text chunks created")
    status: str = Field(default="indexed", description="Processing status")
