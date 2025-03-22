from fastapi import FastAPI, Form, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"]   # Allow all headers
)

@app.get("/")
async def health_check():
    return "Up & Running Successfully"

@app.post("/api")
async def task_runner(question: Optional[str] = Form(None),file: Optional[UploadFile] = File(None)):
    if question is None:
        return {"message": "No question provided"}
    
