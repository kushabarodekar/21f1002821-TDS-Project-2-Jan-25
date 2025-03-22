from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

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
async def task_runner(question: str = Form(None),file: UploadFile = File(None)):
    if question is None:
        return {"message": "No question provided"}
    
