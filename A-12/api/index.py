import os
import sys
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pypdf
import io

# Add the 'code' directory to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'code'))

from orchestrator import Orchestrator

app = FastAPI(title="Multi-Agent Bug Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the orchestrator
orchestrator = Orchestrator()

@app.post("/api/analyze")
async def analyze(
    code_text: str = Form(None),
    context: str = Form(""),
    code_file: UploadFile = File(None)
):
    try:
        extracted_code = ""
        if code_file and code_file.filename:
            content = await code_file.read()
            pdf = pypdf.PdfReader(io.BytesIO(content))
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_code += text + "\n"
        elif code_text:
            extracted_code = code_text
            
        if not extracted_code.strip():
            return {"error": "No code provided. Please enter code or upload a PDF."}

        result = orchestrator.process_single(code=extracted_code, context=context)
        return result
    except Exception as e:
        return {"error": str(e)}

# Serve static files to easily run locally
app.mount("/public", StaticFiles(directory=os.path.join(parent_dir, "public")), name="public")

@app.get("/")
def read_root():
    # Return the index.html for local testing
    index_path = os.path.join(parent_dir, "public", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())
    return {"message": "Hello from API"}
