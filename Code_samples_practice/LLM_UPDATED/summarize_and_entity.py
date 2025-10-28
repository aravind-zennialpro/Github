'''
1. create a virtual environment
    conda create -n LLM python=3.10
    conda activate LLM
2. Set the following as environment variables.
    Gemini api key = [GOOGLE_API_KEY]
    Tavily api key = [TAVILY_API_KEY]
    
    It was set to conda environment variables using
    
    set GOOGLE_API_KEY=[GOOGLE_API_KEY]
    set TAVILY_API_KEY=[TAVILY_API_KEY]
3. Download dependencies
    pip Install google genai,langchain, langchain_community, fastapi,requests,uvicorn, pydantic
    
4. Write a fastapi endpoint that takes text as input and returns the summary of the text. /v1/summarize --> text(paragraph)
 
    Another fastapi endpoint to extract entities from a medical text. /v1/extract/entities
'''


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google import genai

# --- Load Google API key ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY environment variable!")

# --- Initialize Gemini client ---
client = genai.Client(api_key=GOOGLE_API_KEY)

# --- Create FastAPI app ---
app = FastAPI(title="Question -- Summary -- Entity Extraction APP", version="1.0")

# --- Request Models ---
class QuestionInput(BaseModel):
    question: str

class TextInput(BaseModel):
    text: str

# --- Global variable to store latest answer ---
latest_answer = None

# -----------------------------
# 1 Question endpoint
# -----------------------------
@app.post("/v1/question", summary="Ask a question and store its answer automatically")
def ask_question(data: QuestionInput):
    """
    Takes a question and returns an answer.
    The answer will also be stored for automatic summarization.
    """
    global latest_answer

    question_text = data.question.strip()
    if not question_text:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"Answer the following question concisely:\n\n{question_text}"
        )
        answer_text = response.text.strip()

        # Store the latest answer for summarize endpoint
        latest_answer = answer_text

        return {
            "question": question_text,
            "answer": answer_text,
            "message": "Answer stored automatically. You can now call /v1/summarize."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 2 Summarize endpoint (autofill input)
# /v1/summarize --> text(paragraph)
# -----------------------------
@app.get("/v1/summarize", summary="Automatically summarize the latest answer")
def summarize_text():
    """
    Summarizes the answer from the previous /v1/question call automatically.
    """
    global latest_answer

    if not latest_answer:
        raise HTTPException(
            status_code=400,
            detail="No answer found. Please call /v1/question first."
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"Summarize the following text into a short, clear paragraph (4-5 lines):\n\n{latest_answer}"
        )
        summary_text = response.text.strip()

        return {
            "answer": latest_answer,
            "summary": summary_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 3 Extract entities endpoint
# /v1/extract/entities
# -----------------------------
@app.post("/v1/extract_entities", summary="Extract medical entities")
def extract_entities(data: TextInput):
    """
    Extracts medical entities (diseases, drugs, symptoms, treatments) from a text.
    """
    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")

    try:
        prompt = (
            f"Extract medical entities (diseases, drugs, symptoms, treatments, Time) "
            f"and return as JSON with this format:\n"
            f"{{'entities': {{'diseases': [], 'drugs': [], 'symptoms': [], 'treatments': [], 'Time': []}}}}\n\n"
            f"Text:\n\n{text}"
        )
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 4 Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to Question -- Summary -- Entity Extraction API !"
    }
