import logging
import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas.request import UploadResponse
from app.services.rag_service import RAGService
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Global RAG service instance
rag_service = RAGService()


@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and process it for RAG
    
    Args:
        file: PDF file to upload
        
    Returns:
        UploadResponse with file_id, pages, chunks, status
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Create temp directory if not exists
        temp_dir = settings.UPLOAD_DIR
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded file temporarily
        file_path = os.path.join(temp_dir, file.filename)
        contents = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"File uploaded: {file.filename}")
        
        # Load and process PDF
        result = await rag_service.load_pdf(file_path, file.filename)
        
        return UploadResponse(**result)
    
    except ValueError as e:
        logger.error(f"Validation error during upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")



@router.get("/health")
async def health_check():
    """Check upload service health"""
    return {
        "status": "ok",
        "service": "upload",
        "documents_loaded": len(rag_service.documents)
    }
