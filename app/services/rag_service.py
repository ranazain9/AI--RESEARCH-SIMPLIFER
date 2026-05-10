import logging
import uuid
from typing import Dict, Optional
from pathlib import Path

from app.modules.upload.pdf_loader import Loader_
from app.modules.splitter.splitters import Split_Text
from app.modules.vectors.vector import vector_
from app.modules.retriever.retriever_ import retrives
from app.modules.model.models import Model_
from app.modules.config.format_docs import formatDocs
from app.modules.prompts.rag_prompt import RAG_PROMPT

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)


class RAGService:
    """Service for managing RAG pipeline and document queries"""
    
    def __init__(self):
        self.documents: Dict[str, dict] = {}
        self.current_file_id: Optional[str] = None
        self.vector_store = None
        self.retriever = None
        self.chain = None
    
    async def load_pdf(self, file_path: str, filename: str) -> Dict:
        """
        Load and process PDF file
        
        Args:
            file_path: Path to PDF file
            filename: Original filename
            
        Returns:
            Dictionary with file_id, pages, chunks, status
        """
        try:
            # Load PDF
            docs = Loader_.load_pdf(file_path)
            if not docs:
                raise ValueError("No documents loaded from PDF")
            
            # Split into chunks
            chunks = Split_Text(docs)
            if not chunks:
                raise ValueError("No chunks created from documents")
            
            # Create vector store
            self.vector_store = vector_(chunks, Model_.embeddings)
            self.retriever = retrives(self.vector_store)
            
            # Build chain
            self._build_chain()
            
            # Store metadata
            file_id = str(uuid.uuid4())
            self.documents[file_id] = {
                "filename": filename,
                "pages": len(docs),
                "chunks": len(chunks),
                "status": "indexed"
            }
            self.current_file_id = file_id
            
            logger.info(f"Loaded PDF: {filename} (ID: {file_id})")
            
            return {
                "file_id": file_id,
                "filename": filename,
                "pages": len(docs),
                "chunks": len(chunks),
                "status": "indexed"
            }
        
        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise ValueError(f"Failed to load PDF: {str(e)}")
    
    async def query(self, question: str, file_id: Optional[str] = None) -> str:
        """
        Query the loaded paper
        
        Args:
            question: Question to ask
            file_id: Optional file ID (uses current if not provided)
            
        Returns:
            Response from RAG chain
        """
        if not self.chain:
            raise ValueError("No document loaded. Please upload a PDF first.")
        
        if file_id and file_id != self.current_file_id:
            logger.warning(f"Requested file_id {file_id} but current is {self.current_file_id}")
        
        try:
            result = self.chain.invoke(question)
            logger.info(f"Query processed: {question[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Error during query: {str(e)}")
            raise ValueError(f"Failed to process query: {str(e)}")
    
    def _build_chain(self):
        """Build LangChain RAG pipeline"""
        try:
            if not self.retriever:
                raise ValueError("Retriever not initialized")
            
            runnable = RunnableParallel({
                'context': self.retriever | RunnableLambda(formatDocs),
                'question': RunnablePassthrough()
            })
            
            parser = StrOutputParser()
            response_chain = RAG_PROMPT | Model_.groqchat_model() | parser
            self.chain = runnable | response_chain
            logger.info("RAG chain built successfully")
        except Exception as e:
            logger.error(f"Failed to build chain: {str(e)}")
            self.chain = None
            raise ValueError(f"Failed to build RAG chain: {str(e)}")

    
    def get_document_info(self, file_id: str) -> Dict:
        """Get information about a loaded document"""
        if file_id not in self.documents:
            raise ValueError(f"Document with ID {file_id} not found")
        
        return self.documents[file_id]
    
    def list_documents(self) -> Dict[str, dict]:
        """List all loaded documents"""
        return self.documents
    
    def reset_document(self, file_id: Optional[str] = None) -> bool:
        """
        Clear a document from memory
        
        Args:
            file_id: File ID to clear (None = clear current)
            
        Returns:
            True if successful
        """
        target_id = file_id or self.current_file_id
        
        if target_id not in self.documents:
            raise ValueError(f"Document {target_id} not found")
        
        del self.documents[target_id]
        
        if target_id == self.current_file_id:
            self.current_file_id = None
            self.vector_store = None
            self.retriever = None
            self.chain = None
        
        logger.info(f"Document {target_id} cleared")
        return True
    
    def is_ready(self) -> bool:
        """Check if service is ready for queries"""
        return self.chain is not None
