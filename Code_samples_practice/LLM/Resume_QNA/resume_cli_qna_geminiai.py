import os
import faiss
import numpy as np
import fitz  # PyMuPDF
import google.generativeai as genai
from pymongo import MongoClient

# -------------------- Configuration --------------------
PDF_FOLDER = "resumes"
FAISS_INDEX_FILE = "resume_index.faiss"
INDEX_DATA_FILE = "resume_chunks.npy"

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ameet:eyqKJ3E3b7ie2OFA@resumestore.c6xamui.mongodb.net/")
DB_NAME = "resume_manager"
COLLECTION_NAME = "resumes"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB6tX62PZ4haW57O_AVR3WpLTHFj_9Vifg")  # Replace this with your key or keep it in env

# -------------------- Initialization --------------------
genai.configure(api_key=GEMINI_API_KEY)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
resume_collection = db[COLLECTION_NAME]

embedding_dim = 768  # Gemini returns 768-dimensional vectors
index = faiss.IndexFlatL2(embedding_dim)
index_data = []


# -------------------- Utility Functions --------------------

def load_index():
    global index, index_data
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
        print("Loaded FAISS index from file.")
    if os.path.exists(INDEX_DATA_FILE):
        index_data = np.load(INDEX_DATA_FILE, allow_pickle=True).tolist()
        print("Loaded index data from file.")


def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    np.save(INDEX_DATA_FILE, index_data)
    print("Saved FAISS index and index data.")


def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in pdf_document])


def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def get_gemini_embeddings(text):
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return response['embedding']
    except Exception as e:
        print(f"Embedding Error: {e}")
        return np.zeros((768,), dtype="float32")  # Gemini embeddings are 768-d


# -------------------- Main Logic --------------------

def index_resumes():
    global index_data
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            if resume_collection.find_one({"_id": filename}):
                print(f"Skipping: {filename} - already indexed")
                continue

            text = load_pdf_text(os.path.join(PDF_FOLDER, filename))
            chunks = chunk_text(text)
            for chunk in chunks:
                embedding = get_gemini_embeddings(chunk)
                if embedding is not None:
                    index.add(np.array([embedding], dtype="float32"))
                    index_data.append({"_id": filename, "chunk": chunk})
            resume_collection.insert_one({"_id": filename, "text": text})
            print(f"Indexed resume: {filename}")
    save_index()


def query_resume(query):
    if index.ntotal == 0 or len(index_data) == 0:
        print("No resumes are indexed. Please use Option 1 first.")
        return

    query_vector = get_gemini_embeddings(query)
    D, I = index.search(np.array([query_vector], dtype="float32"), 3)

    matched_chunks = []
    for i in I[0]:
        if i < len(index_data):
            matched_chunks.append(index_data[i]["chunk"])

    combined_context = "\n".join(matched_chunks)

    # Use Gemini Pro for final answer
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"Here is a resume:\n\n{combined_context}\n\nQuestion: {query}"
        )
        print("\nAnswer:")
        print(response.text)
    except Exception as e:
        print(f"Gemini Pro Error: {e}")



# -------------------- Main Menu --------------------

def main():
    load_index()
    while True:
        print("\nGemini AI Resume QnA System")
        print("1. Process resumes in folder")
        print("2. Ask questions")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            index_resumes()
        elif choice == "2":
            query = input("Ask your question: ")
            query_resume(query)
        elif choice == "3":
            print("Goodbye... See you again.")
            break
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
