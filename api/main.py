from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import requests
import os

API_KEY = os.getenv("AIPROXY_TOKEN")

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

META_PROMPT = """
Assume you are Intelligent student whose objective is to prepare a clear and concise prompt that an LLM can understand and solve or calculate the final result of the given question or task.
Given a question or task description, produce a detailed system prompt to guide a language model in solving the question or task effectively.

# Guidelines
- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data  bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")
""".strip()

@app.post("/api")
async def task_runner(question: Optional[str] = Form(None),file: Optional[UploadFile] = File(None)):
    if question is None:
        return {"message": "No question provided"}

    prompt = queryLLM(question)
    return getFinalResult(prompt)

def queryLLM(query):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        data = {"model": "gpt-4o-mini", 
                "messages": [{"role": "system","content": META_PROMPT},{"role": "user", "content": query}]
                }
        response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/chat/completions", headers=headers, json=data)
    except Exception as e:
        if 400 <= response.status_code < 500:
            print(str(e))
            raise HTTPException(status_code=400, detail="Bad Request : "+response.text+str(e))
        else:
            print(str(e))
            raise HTTPException(status_code=500, detail="Internal Server Error "+response.text+str(e))
    response.raise_for_status() 
    return response.json()["choices"][0]["message"]["content"].strip()
    
def getFinalResult(prompt):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        data = {"model": "gpt-4o-mini", 
                "messages": [{"role": "user", "content": prompt}]
                }
        response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/chat/completions", headers=headers, json=data)
    except Exception as e:
        if 400 <= response.status_code < 500:
            print(str(e))
            raise HTTPException(status_code=400, detail="Bad Request : "+response.text+str(e))
        else:
            print(str(e))
            raise HTTPException(status_code=500, detail="Internal Server Error "+response.text+str(e))
    response.raise_for_status() 
    return response.json()["choices"][0]["message"]["content"].strip()
