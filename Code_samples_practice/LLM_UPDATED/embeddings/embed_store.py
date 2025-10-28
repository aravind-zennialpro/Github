# embeddings_generator.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# -------------------------
# 1. Google API Key
# -------------------------
GOOGLE_API_KEY = "AIzaSyDYSHZ_nMKHdZEGrqwHo_87YqmngXh9Nxg"  # Replace with your key

# -------------------------
# 2. Sample texts to embed
# -------------------------
texts = [
    "Hello, I am testing embeddings.",
    "LangChain makes working with LLMs easier.",
    "FAISS allows fast similarity search."
]

# -------------------------
# 3. Create embeddings object
# -------------------------
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# -------------------------
# 4. Generate embeddings for multiple texts
# -------------------------
embeddings = embeddings_model.embed_documents(texts)

# -------------------------
# 5. Print embeddings length for each text
# -------------------------
for i, emb in enumerate(embeddings):
    print(f"Text: {texts[i]}")
    print(f"Embedding length: {len(emb)}\n")
