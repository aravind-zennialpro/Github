from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np

GOOGLE_API_KEY = "AIzaSyDYSHZ_nMKHdZEGrqwHo_87YqmngXh9Nxg"

emb_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Two sample texts
text1 = "what are you doing?"
text2 = "what is your plan?"

# Get embeddings
emb1 = emb_model.embed_query(text1)
emb2 = emb_model.embed_query(text2)
print(emb1)
print(emb2)
# Cosine similarity
cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
print("Cosine similarity:", cos_sim)
