# FastAPI Routes Documentation

## Overview
This document describes the FastAPI routes for the AI Research Paper Simplifier application.

## Base URL
```
http://localhost:8000
```

## API Routes

### 1. Health Check
**GET** `/health`

Check if the API is running and pipeline is ready.

**Response:**
```json
{
  "status": "ok",
  "service": "AI Research Paper Simplifier",
  "pipeline_ready": false,
  "upload_dir": "/tmp/paper_uploads"
}
```

---

### 2. Upload PDF
**POST** `/api/upload/`

Upload a PDF file for processing and indexing.

**Request:**
- Body: `FormData` with file field
- Content-Type: `multipart/form-data`

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/upload/" \
  -F "file=@path/to/paper.pdf"
```

**Example using Python:**
```python
import requests

with open("paper.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/api/upload/", files=files)
    print(response.json())
```

**Response:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "Lecun2015.pdf",
  "pages": 10,
  "chunks": 45,
  "status": "indexed"
}
```

---

### 3. Query Paper
**POST** `/api/query/`

Query an uploaded research paper.

**Request Body:**
```json
{
  "question": "What is the main topic of the paper?",
  "file_id": "550e8400-e29b-41d4-a716-446655440000"  // optional
}
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "file_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Example using Python:**
```python
import requests

data = {
    "question": "Explain the methodology",
    "file_id": "550e8400-e29b-41d4-a716-446655440000"
}
response = requests.post("http://localhost:8000/api/query/", json=data)
print(response.json())
```

**Response:**
```json
{
  "question": "What is the main topic of the paper?",
  "simple_explanation": "This is a simplified explanation...",
  "technical_details": "",
  "methodology": "",
  "equations": "",
  "visual_architecture": "",
  "key_points": [],
  "citations": []
}
```

---

### 4. List Documents
**GET** `/api/query/documents`

List all uploaded documents currently in memory.

**Example using cURL:**
```bash
curl "http://localhost:8000/api/query/documents"
```

**Response:**
```json
{
  "count": 1,
  "documents": {
    "550e8400-e29b-41d4-a716-446655440000": {
      "filename": "Lecun2015.pdf",
      "pages": 10,
      "chunks": 45,
      "status": "indexed"
    }
  },
  "current_file_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 5. Get Document Info
**GET** `/api/query/documents/{file_id}`

Get detailed information about a specific document.

**Parameters:**
- `file_id` (path): The file ID returned from upload

**Example using cURL:**
```bash
curl "http://localhost:8000/api/query/documents/550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "Lecun2015.pdf",
  "pages": 10,
  "chunks": 45,
  "indexed": true
}
```

---

### 6. Delete Document
**DELETE** `/api/query/documents/{file_id}`

Delete a document and clear it from memory.

**Parameters:**
- `file_id` (path): The file ID to delete

**Example using cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/query/documents/550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "status": "deleted",
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Document 550e8400-e29b-41d4-a716-446655440000 has been removed"
}
```

---

### 7. Query Health
**GET** `/api/query/health`

Check query service health.

**Response:**
```json
{
  "status": "ok",
  "service": "query",
  "pipeline_ready": true,
  "documents_loaded": 1
}
```

---

### 8. Upload Health
**GET** `/api/upload/health`

Check upload service health.

**Response:**
```json
{
  "status": "ok",
  "service": "upload",
  "documents_loaded": 1
}
```

---

## Running the Server

### Using Uvicorn

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Python

```bash
python main.py
```

---

## Interactive Documentation

Once the server is running, access:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- **200 OK**: Request successful
- **400 Bad Request**: Invalid input or missing document
- **404 Not Found**: Document not found
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Workflow Example

1. **Upload a paper:**
   ```bash
   curl -X POST "http://localhost:8000/api/upload/" \
     -F "file=@paper.pdf"
   ```
   Save the returned `file_id`.

2. **Query the paper:**
   ```bash
   curl -X POST "http://localhost:8000/api/query/" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the topic?", "file_id": "YOUR_FILE_ID"}'
   ```

3. **Get document list:**
   ```bash
   curl "http://localhost:8000/api/query/documents"
   ```

4. **Delete when done:**
   ```bash
   curl -X DELETE "http://localhost:8000/api/query/documents/YOUR_FILE_ID"
   ```
