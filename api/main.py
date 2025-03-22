from fastapi import FastAPI

API_KEY = os.getenv("AIPROXY_TOKEN")

app = FastAPI()

@app.get("/")
async def health_check():
    return "Up & Running Successfully "+API_KEY
