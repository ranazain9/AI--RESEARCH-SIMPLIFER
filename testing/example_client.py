"""
Example: Using the AI Research Paper Simplifier API from Python

This file demonstrates how to interact with the FastAPI endpoints
using Python requests library.
"""

import requests
import json
from typing import Optional


class PaperSimplifierClient:
    """Client for interacting with Paper Simplifier API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_file_id = None
    
    # ============ HEALTH & STATUS ============
    
    def check_health(self) -> dict:
        """Check if API is healthy"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    # ============ UPLOAD ============
    
    def upload_paper(self, pdf_path: str) -> Optional[str]:
        """
        Upload a PDF paper
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            file_id if successful, None otherwise
        """
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(
                f"{self.base_url}/api/upload/",
                files=files
            )
        
        response.raise_for_status()
        result = response.json()
        self.current_file_id = result["file_id"]
        return result["file_id"]
    
    # ============ QUERY ============
    
    def ask_question(
        self,
        question: str,
        file_id: Optional[str] = None
    ) -> dict:
        """
        Ask a question about the uploaded paper
        
        Args:
            question: The question to ask
            file_id: Optional file ID (uses current if not provided)
            
        Returns:
            Query response with analysis
        """
        if not file_id:
            file_id = self.current_file_id
        
        if not file_id:
            raise ValueError("No file_id available. Upload a paper first.")
        
        payload = {
            "question": question,
            "file_id": file_id
        }
        
        response = self.session.post(
            f"{self.base_url}/api/query/",
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    # ============ DOCUMENT MANAGEMENT ============
    
    def list_documents(self) -> dict:
        """List all loaded documents"""
        response = self.session.get(f"{self.base_url}/api/query/documents")
        response.raise_for_status()
        return response.json()
    
    def get_document_info(self, file_id: str) -> dict:
        """Get info about a specific document"""
        response = self.session.get(
            f"{self.base_url}/api/query/documents/{file_id}"
        )
        response.raise_for_status()
        return response.json()
    
    def delete_paper(self, file_id: Optional[str] = None) -> dict:
        """Delete a paper from memory"""
        if not file_id:
            file_id = self.current_file_id
        
        if not file_id:
            raise ValueError("No file_id provided")
        
        response = self.session.delete(
            f"{self.base_url}/api/query/documents/{file_id}"
        )
        
        response.raise_for_status()
        
        if file_id == self.current_file_id:
            self.current_file_id = None
        
        return response.json()


# ============ EXAMPLE USAGE ============

def example_1_basic_workflow():
    """Example 1: Basic workflow"""
    print("=" * 60)
    print("Example 1: Basic Workflow")
    print("=" * 60)
    
    # Initialize client
    client = PaperSimplifierClient()
    
    # Check health
    print("\n1. Checking API health...")
    health = client.check_health()
    print(f"   Status: {health['status']}")
    print(f"   Pipeline ready: {health['pipeline_ready']}")
    
    # Upload paper
    print("\n2. Uploading paper...")
    pdf_path = r"D:\AI Research Paper Simplifier\Lecun2015.pdf"
    file_id = client.upload_paper(pdf_path)
    print(f"   File uploaded with ID: {file_id}")
    
    # Ask question
    print("\n3. Asking question about paper...")
    response = client.ask_question("What is the main topic of this paper?")
    print(f"   Question: {response['question']}")
    print(f"   Answer: {response['simple_explanation'][:200]}...")
    
    # List documents
    print("\n4. Listing documents...")
    docs = client.list_documents()
    print(f"   Found {docs['count']} document(s)")
    
    # Clean up
    print("\n5. Deleting paper...")
    result = client.delete_paper()
    print(f"   Status: {result['status']}")


def example_2_multiple_questions():
    """Example 2: Ask multiple questions"""
    print("\n" + "=" * 60)
    print("Example 2: Multiple Questions")
    print("=" * 60)
    
    client = PaperSimplifierClient()
    
    # Upload
    print("\nUploading paper...")
    pdf_path = r"D:\AI Research Paper Simplifier\Lecun2015.pdf"
    file_id = client.upload_paper(pdf_path)
    
    # Ask multiple questions
    questions = [
        "What is the main contribution?",
        "What is the methodology?",
        "What are the results?",
        "What is the conclusion?"
    ]
    
    print("\nAsking multiple questions...")
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question}")
        response = client.ask_question(question)
        # Print first 150 chars of answer
        answer = response['simple_explanation']
        print(f"   {answer[:150]}...")
    
    # Clean up
    client.delete_paper()


def example_3_error_handling():
    """Example 3: Error handling"""
    print("\n" + "=" * 60)
    print("Example 3: Error Handling")
    print("=" * 60)
    
    client = PaperSimplifierClient()
    
    # Try to query without uploading
    print("\n1. Trying to query without uploading...")
    try:
        client.ask_question("What is this?")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")
    
    # Try to delete non-existent document
    print("\n2. Trying to delete non-existent document...")
    try:
        client.delete_paper("fake-id")
    except requests.exceptions.HTTPError as e:
        print(f"   ✓ Caught error: {e.response.status_code} - {e.response.text}")
    
    # Try to upload non-existent file
    print("\n3. Trying to upload non-existent file...")
    try:
        client.upload_paper("non_existent.pdf")
    except FileNotFoundError as e:
        print(f"   ✓ Caught error: {e}")


def example_4_batch_processing():
    """Example 4: Batch processing multiple papers"""
    print("\n" + "=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    # Note: This example shows the pattern, but we only have one PDF
    papers = [
        (r"D:\AI Research Paper Simplifier\Lecun2015.pdf", "Lecun2015"),
    ]
    
    results = {}
    
    for pdf_path, paper_name in papers:
        print(f"\nProcessing {paper_name}...")
        
        client = PaperSimplifierClient()
        
        try:
            # Upload
            file_id = client.upload_paper(pdf_path)
            print(f"  ✓ Uploaded")
            
            # Get info
            info = client.get_document_info(file_id)
            print(f"  Pages: {info['pages']}, Chunks: {info['chunks']}")
            
            # Ask question
            response = client.ask_question("What is the main topic?")
            results[paper_name] = response
            
            # Clean up
            client.delete_paper()
            print(f"  ✓ Processed and cleaned up")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\nResults summary:")
    for name, result in results.items():
        print(f"  {name}: {result['question']}")


# ============ DIRECT API CALLS ============

def direct_api_example():
    """Example: Direct API calls using requests"""
    print("\n" + "=" * 60)
    print("Direct API Calls Example")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Check health
    print("\n1. GET /health")
    response = requests.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=4)}")
    
    # Upload file
    print("\n2. POST /api/upload/")
    pdf_path = r"D:\AI Research Paper Simplifier\Lecun2015.pdf"
    with open(pdf_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{base_url}/api/upload/", files=files)
    
    print(f"   Status: {response.status_code}")
    result = response.json()
    file_id = result["file_id"]
    print(f"   File ID: {file_id}")
    
    # Query
    print("\n3. POST /api/query/")
    payload = {"question": "What is the topic?", "file_id": file_id}
    response = requests.post(
        f"{base_url}/api/query/",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Answer: {response.json()['simple_explanation'][:100]}...")
    
    # Delete
    print("\n4. DELETE /api/query/documents/{file_id}")
    response = requests.delete(f"{base_url}/api/query/documents/{file_id}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()['status']}")


if __name__ == "__main__":
    import sys
    
    print("\nAI Research Paper Simplifier - Python Client Examples\n")
    print("Choose an example to run:")
    print("  1. Basic workflow")
    print("  2. Multiple questions")
    print("  3. Error handling")
    print("  4. Batch processing")
    print("  5. Direct API calls")
    print("  0. Exit")
    
    choice = input("\nEnter choice (0-5): ").strip()
    
    try:
        if choice == "1":
            example_1_basic_workflow()
        elif choice == "2":
            example_2_multiple_questions()
        elif choice == "3":
            example_3_error_handling()
        elif choice == "4":
            example_4_batch_processing()
        elif choice == "5":
            direct_api_example()
        elif choice == "0":
            sys.exit(0)
        else:
            print("Invalid choice")
    
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure:")
        print("1. The API server is running (uvicorn main:app --reload)")
        print("2. The PDF file exists at the specified path")
        print("3. Your GROQ_API_KEY is set in .env")
