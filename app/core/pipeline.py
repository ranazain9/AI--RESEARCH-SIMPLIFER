import logging
import os
from typing import Optional
from pathlib import Path
from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Orchestrates the RAG pipeline for paper analysis"""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"RAG Pipeline initialized. Upload dir: {self.upload_dir}")
    
    def get_upload_path(self, filename: str) -> str:
        """Get safe path for uploaded file"""
        safe_filename = Path(filename).name
        return str(self.upload_dir / safe_filename)
    
    def is_ready(self) -> bool:
        """Check if pipeline is ready"""
        return self.upload_dir.exists()

