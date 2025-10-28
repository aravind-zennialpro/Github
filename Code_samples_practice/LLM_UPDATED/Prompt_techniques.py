'''
Q1: Create additional fastapi endpoints for each:
 
        1. zero shot: Ask the model to perform a task without giving examples.
        2. Few shot prompting: Give a few examples to help the model understand the pattern.
        3. chain of thought: Ask the model to explain its reasoning step-by-step.

Q2: pdf file handling

'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai

# --- Load Google API key ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY environment variable!")

# --- Initialize Gemini client ---
genai.configure(api_key=GOOGLE_API_KEY)

# --- Create FastAPI app ---
app = FastAPI(title="Prompt Strategies and Techniques API", version="1.0")

# --- Request Model ---
class PromptRequest(BaseModel):
    prompt: str

# -----------------------------
# 1 Zero-Shot Prompt Endpoint
# -----------------------------
@app.post("/zero")
async def zero_shot(prompt_request: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-2.0-pro" if available
        response = model.generate_content(prompt_request.prompt)

        # Extract the model output
        output_text = response.text if hasattr(response, "text") else str(response)

        return {"Zero-shot prompt": prompt_request.prompt, "response": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# 2 Few-Shot Prompt Endpoint
# -----------------------------
@app.post("/few")
async def few_shot(prompt_request: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-2.0-pro" if available
        response = model.generate_content(prompt_request.prompt)

        # Extract the model output
        output_text = response.text if hasattr(response, "text") else str(response)

        return {"Few-shot prompt": prompt_request.prompt, "response": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# 3 Chain-of-thought Prompt Endpoint
# -----------------------------
@app.post("/Chain-of-thought")
async def Chain_of_thought(prompt_request: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-2.0-pro" if available
        response = model.generate_content(prompt_request.prompt)

        # Extract the model output
        output_text = response.text if hasattr(response, "text") else str(response)

        return {"Chain-of-thought prompt": prompt_request.prompt, "response": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# -----------------------------
# 4 Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to Prompt Techniques API!"}
