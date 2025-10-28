'''
Q2: PDF file handling
 
'''

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pathlib
import os
from google import genai
from google.genai import types

# Initialize FastAPI app
app = FastAPI(title="PDF Handler API")

# Initialize Gemini client
client = genai.Client()

# Store the uploaded file reference globally
uploaded_pdf_file = None

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to PDF Analyser!"}

# -----------------------------
#  Uploading the PDF:
# -----------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and store it using Gemini File API.
    """
    global uploaded_pdf_file

    # Save the uploaded file temporarily
    file_path = pathlib.Path(f"./{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Upload the file to Gemini
    uploaded_pdf_file = client.files.upload(file=file_path)

    # Optionally remove local copy after upload
    os.remove(file_path)

    return JSONResponse({
        "status": "success",
        "message": f"PDF '{file.filename}' uploaded successfully!"
    })

# -----------------------------
#  Asking QUestion on PDF:
# -----------------------------
@app.post("/ask_pdf")
async def ask_pdf(prompt: str = Form(...)):
    """
    Ask a question related to the uploaded PDF using Gemini model.
    """
    global uploaded_pdf_file

    if uploaded_pdf_file is None:
        return JSONResponse({
            "status": "error",
            "message": "No PDF uploaded yet. Please upload one first."
        }, status_code=400)

    # Generate AI response using Gemini
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[uploaded_pdf_file, prompt]
    )

    return JSONResponse({
        "status": "success",
        "prompt": prompt,
        "response": response.text
    })
