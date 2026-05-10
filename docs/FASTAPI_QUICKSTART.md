# FastAPI Quick Start Guide

## Prerequisites
- Python 3.8+
- All dependencies from `requirements.txt` installed
- `.env` file with `GROQ_API_KEY` set

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
pip list | grep -i fastapi
pip list | grep -i uvicorn
```

---

## Starting the Server

### Option 1: Using Uvicorn (Recommended for Development)
```bash
# With auto-reload on code changes
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or with more verbose logging
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### Option 2: Using Python
```bash
python main.py
```

### Output
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO: AI Research Paper Simplifier API
INFO:     Application startup complete.
```

---

## Accessing the API

### 1. Interactive Documentation
Once the server is running, open in your browser:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 2. Test Health
```bash
curl http://localhost:8000/health
```

---

## Basic Workflow

### Step 1: Upload a PDF
```bash
curl -X POST "http://localhost:8000/api/upload/" \
  -F "file=@Lecun2015.pdf"
```

Save the `file_id` from response.

### Step 2: Query the Paper
```bash
curl -X POST "http://localhost:8000/api/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "file_id": "YOUR_FILE_ID_HERE"
  }'
```

### Step 3: List Documents
```bash
curl "http://localhost:8000/api/query/documents"
```

### Step 4: Delete Document (Optional)
```bash
curl -X DELETE "http://localhost:8000/api/query/documents/YOUR_FILE_ID_HERE"
```

---

## Running Tests

### 1. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. In a New Terminal, Run Tests
```bash
python test_api.py
```

---

## Project Structure

```
d:\AI Research Paper Simplifier\
├── main.py                 # FastAPI app entry point
├── test_api.py            # Test script
├── requirements.txt       # Dependencies
├── FASTAPI_ROUTES.md      # API documentation
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── upload.py  # PDF upload endpoints
│   │   │   └── query.py   # Query endpoints
│   ├── schemas/
│   │   ├── request.py     # Pydantic request models
│   │   └── response.py    # Pydantic response models
│   ├── services/
│   │   └── rag_service.py # RAG logic
│   └── core/
│       └── pipeline.py    # Pipeline orchestration
├── upload/                # Original modules
├── splitter/
├── vectors/
├── retriever/
├── model/
└── PROMPT/
```

---

## Common Issues & Fixes

### Issue: Port Already in Use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Issue: Module Not Found
```bash
# Make sure you're in the correct directory
cd d:\AI Research Paper Simplifier

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: GROQ_API_KEY Not Found
```bash
# Create .env file with:
GROQ_API_KEY=your_key_here
```

### Issue: PDF Upload Fails
- Check file is actually a PDF
- Check file size (should be reasonable)
- Check disk space

---

## Environment Variables

Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Production Deployment

### Using Gunicorn + Uvicorn
```bash
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t paper-simplifier .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key paper-simplifier
```

---

## Next Steps

1. Review [FASTAPI_ROUTES.md](FASTAPI_ROUTES.md) for detailed endpoint documentation
2. Run `test_api.py` to verify everything works
3. Build your frontend/client to consume the API
4. Deploy to production when ready

---

## Support

For issues or questions:
1. Check logs: `uvicorn main:app --reload --log-level debug`
2. Review error responses from API
3. Check `.env` file is configured correctly
4. Verify all dependencies are installed
