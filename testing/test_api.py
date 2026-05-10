"""
FastAPI Test Script
Test all endpoints of the AI Research Paper Simplifier API
"""

import requests
import json
from pathlib import Path


class PaperSimplifierClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.file_id = None
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        print("Health Check:")
        print(json.dumps(response.json(), indent=2))
        return response
    
    def upload_pdf(self, pdf_path: str) -> str:
        """Upload a PDF file"""
        if not Path(pdf_path).exists():
            print(f"Error: File {pdf_path} not found")
            return None
        
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{self.base_url}/api/upload/", files=files)
        
        print(f"\nUpload Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2))
        
        if response.status_code == 200:
            self.file_id = result.get("file_id")
            print(f"✓ File uploaded successfully. File ID: {self.file_id}")
            return self.file_id
        else:
            print("✗ Upload failed")
            return None
    
    def query_paper(self, question: str, file_id: str = None) -> str:
        """Query the uploaded paper"""
        if not file_id:
            file_id = self.file_id
        
        if not file_id:
            print("Error: No file_id available. Upload a paper first.")
            return None
        
        payload = {
            "question": question,
            "file_id": file_id
        }
        
        response = requests.post(
            f"{self.base_url}/api/query/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nQuery Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2))
        
        return response
    
    def list_documents(self):
        """List all loaded documents"""
        response = requests.get(f"{self.base_url}/api/query/documents")
        
        print("\nDocuments List:")
        print(json.dumps(response.json(), indent=2))
        return response
    
    def get_document_info(self, file_id: str):
        """Get info about specific document"""
        response = requests.get(f"{self.base_url}/api/query/documents/{file_id}")
        
        print(f"\nDocument Info ({file_id}):")
        print(json.dumps(response.json(), indent=2))
        return response
    
    def delete_document(self, file_id: str = None):
        """Delete a document"""
        if not file_id:
            file_id = self.file_id
        
        if not file_id:
            print("Error: No file_id provided")
            return None
        
        response = requests.delete(f"{self.base_url}/api/query/documents/{file_id}")
        
        print(f"\nDelete Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print(f"✓ Document deleted successfully")
            self.file_id = None
        
        return response


def main():
    """Run tests"""
    print("=" * 60)
    print("AI Research Paper Simplifier - API Test Suite")
    print("=" * 60)
    
    client = PaperSimplifierClient()
    
    # 1. Health check
    print("\n1. Testing Health Check...")
    client.health_check()
    
    # 2. Upload PDF
    print("\n2. Testing PDF Upload...")
    pdf_path = r"D:\AI Research Paper Simplifier\Lecun2015.pdf"
    
    file_id = client.upload_pdf(pdf_path)
    if not file_id:
        print("Cannot proceed without uploaded file")
        return
    
    # 3. List documents
    print("\n3. Testing List Documents...")
    client.list_documents()
    
    # 4. Get document info
    print("\n4. Testing Get Document Info...")
    client.get_document_info(file_id)
    
    # 5. Query paper
    print("\n5. Testing Query Paper...")
    questions = [
        "What is the main topic of the paper?",
        "What is the methodology?",
        "What are the key findings?"
    ]
    
    for q in questions:
        print(f"\n   Query: {q}")
        try:
            client.query_paper(q, file_id)
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to API. Is the server running?")
            break
    
    # 6. Delete document
    print("\n6. Testing Delete Document...")
    client.delete_document(file_id)
    
    # 7. Verify deletion
    print("\n7. Verifying Deletion...")
    client.list_documents()
    
    print("\n" + "=" * 60)
    print("Test Suite Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
