import logging
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse, DocumentInfo
from app.services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

# Use same instance as upload
from app.api.routes.upload import rag_service


@router.post("/", response_model=QueryResponse)
async def query_paper(request: QueryRequest):
    """
    Query an uploaded research paper
    
    Args:
        request: QueryRequest with question and optional file_id
        
    Returns:
        QueryResponse with comprehensive paper analysis
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Query the RAG service
        result = await rag_service.query(request.question, request.file_id)
        
        # Parse result into structured response
        # For now, return raw result - can be enhanced with better parsing
        response = QueryResponse(
            question=request.question,
            simple_explanation=result,
            technical_details="",
            methodology="",
            equations="",
            visual_architecture="",
            key_points=[],
            citations=[]
        )
        
        logger.info(f"Query processed successfully")
        return response
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")


@router.get("/documents", response_model=dict)
async def list_documents():
    """List all loaded documents"""
    return {
        "loaded_documents": rag_service.documents,
        "current_file_id": rag_service.current_file_id,
        "chain_ready": rag_service.chain is not None,
        "vector_store_ready": rag_service.vector_store is not None,
        "retriever_ready": rag_service.retriever is not None
    }


@router.get("/documents/{file_id}", response_model=DocumentInfo)
async def get_document_info(file_id: str):
    """Get information about a specific document"""
    try:
        doc_info = rag_service.get_document_info(file_id)
        return DocumentInfo(
            file_id=file_id,
            **doc_info
        )
    except ValueError as e:
        logger.error(f"Document not found: {file_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving document info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{file_id}")
async def delete_document(file_id: str):
    """Delete a document and clear it from memory"""
    try:
        rag_service.reset_document(file_id)
        return {
            "status": "deleted",
            "file_id": file_id,
            "message": f"Document {file_id} has been removed"
        }
    except ValueError as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error during document deletion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check query service health"""
    return {
        "status": "ok",
        "service": "query",
        "pipeline_ready": rag_service.is_ready(),
        "documents_loaded": len(rag_service.documents)
    }
