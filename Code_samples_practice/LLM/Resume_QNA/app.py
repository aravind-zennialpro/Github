import os
import fitz  # PyMuPDF
import faiss
import numpy as np
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# -------------------- Load .env --------------------
load_dotenv()
API_KEY = os.getenv("API_KEY")
print("API Key Loaded:", "yes" if API_KEY else "No MISSING")

# -------------------- Configuration --------------------
PDF_FOLDER = "resumes"
FAISS_INDEX_FILE = "resume_index.faiss"
INDEX_DATA_FILE = "resume_chunks.npy"
DB_NAME = "resume_manager"
COLLECTION_NAME = "resumes"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"
embedding_dim = 1536

# -------------------- Mongo + FAISS Init --------------------
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
resume_collection = db[COLLECTION_NAME]

index = faiss.IndexFlatL2(embedding_dim)
index_data = []

# -------------------- FAISS Helpers --------------------
def load_index():
    global index, index_data
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
        print("FAISS index loaded.")
    if os.path.exists(INDEX_DATA_FILE):
        index_data.extend(np.load(INDEX_DATA_FILE, allow_pickle=True).tolist())
        print("Chunk data loaded.")

def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    np.save(INDEX_DATA_FILE, index_data)
    print("Index and data saved.")

# -------------------- Resume Load + Chunk --------------------
def load_pdf_text(pdf_path):
    try:
        pdf = fitz.open(pdf_path)
        return "\n".join([page.get_text() for page in pdf])
    except Exception as e:
        print(f"Failed to load {pdf_path}: {e}")
        return ""

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# -------------------- Embedding Using chatanywhere.tech --------------------
def get_openai_embedding(text):
    try:
        response = requests.post(
            "https://api.chatanywhere.tech/v1/embeddings",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": EMBEDDING_MODEL,
                "input": text
            }
        )
        response.raise_for_status()
        embedding = response.json()["data"][0]["embedding"]

        if len(embedding) != embedding_dim:
            print(f"Embedding dimension mismatch: got {len(embedding)}, expected {embedding_dim}")
            return None

        return np.array(embedding, dtype="float32")
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

# -------------------- Resume Indexer --------------------
def index_resumes():
    global index_data
    print("\nIndexing resumes from:", PDF_FOLDER)

    for filename in os.listdir(PDF_FOLDER):
        if not filename.endswith(".pdf"):
            continue

        if resume_collection.find_one({"_id": filename}):
            print(f"Skipping {filename} (already indexed)")
            continue

        full_path = os.path.join(PDF_FOLDER, filename)
        text = load_pdf_text(full_path)
        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = get_openai_embedding(chunk)
            if embedding is not None and embedding.shape[0] == embedding_dim:
                index.add(np.array([embedding], dtype="float32"))
                index_data.append({"_id": filename, "chunk": chunk})
            else:
                print(f"Skipped a chunk in {filename} due to invalid embedding.")

        resume_collection.insert_one({"_id": filename, "text": text})
        print(f"Indexed: {filename}")

    save_index()

# -------------------- Resume QnA Chat --------------------
def query_resume(query):
    if index.ntotal == 0 or not index_data:
        print("No resumes indexed. Please run Option 1 first.")
        return

    query_vector = get_openai_embedding(query)

    if query_vector is None or query_vector.shape[0] != embedding_dim:
        print(f"Invalid query vector shape: {query_vector.shape if query_vector is not None else 'None'}")
        return

    print(f"query vector shape: {query_vector.shape}")
    print(f"FAISS expects: {index.d}")

    D, I = index.search(np.array([query_vector], dtype="float32"), 3)

    matched_chunks = [index_data[i]["chunk"] for i in I[0] if i < len(index_data)]
    context = "\n".join(matched_chunks)

    try:
        response = requests.post(
            "https://api.chatanywhere.tech/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": CHAT_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant analyzing resumes to answer user questions."
                    },
                    {
                        "role": "user",
                        "content": f"Resume:\n{context}\n\nQuestion: {query}"
                    }
                ],
                "temperature": 0.2
            }
        )
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"].strip()
        print("\nAnswer:\n", answer)
    except Exception as e:
        print(f"Chat Error: {e}")

# -------------------- CLI --------------------
def main():
    load_index()
    while True:
        print("\n=== Resume QnA ===")
        print("1. Index resumes")
        print("2. Ask a question")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            index_resumes()
        elif choice == "2":
            query = input("Enter your question: ")
            query_resume(query)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try 1, 2 or 3.")

if __name__ == "__main__":
    main()
