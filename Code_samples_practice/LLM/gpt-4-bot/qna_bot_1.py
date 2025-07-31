import os
import json
import fitz
import openai
import numpy as np
import faiss
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE = 50
EMBED_MODEL = "text-embedding-3-small"
INDEX_FILE_PATH = "faiss.index"
CHUNKS_FILE_PATH = "chunks_store.json"

index = None
chunks = []


def load_chunks():
    global chunks
    if os.path.exists(CHUNKS_FILE_PATH):
        with open(CHUNKS_FILE_PATH, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    else:
        chunks = []


def save_chunks():
    with open(CHUNKS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f)


def embed_chunks(chunk_list):
    embeddings = openai.embeddings.create(model=EMBED_MODEL, input=chunk_list)
    vectors = np.array([e.embedding for e in embeddings.data]).astype("float32")
    return vectors


def chunk_text(text):
    words = text.split()
    return [" ".join(words[i: i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]


def extract_text_from_pdf(pdf_path):
    pages = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text() for page in pages])
    return full_text


def add_document():
    global index, chunks

    pdf_path = input("Enter path of PDF file: ").strip()
    if not os.path.exists(pdf_path):
        print(f"File not found at {pdf_path}")
        return

    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print("No content found. Try another PDF file.")
        return

    new_chunks = chunk_text(text)
    new_vectors = embed_chunks(new_chunks)

    if os.path.exists(INDEX_FILE_PATH):
        index = faiss.read_index(INDEX_FILE_PATH)
    else:
        index = faiss.IndexFlatL2(new_vectors.shape[1])

    index.add(new_vectors)
    faiss.write_index(index, INDEX_FILE_PATH)

    # Append to global chunks list and persist
    chunks.extend(new_chunks)
    save_chunks()

    print("Document indexed successfully.")


def search_faiss_index(query_vector, index):
    distance, indices = index.search(query_vector, 5)
    return indices[0]


def ask_gpt4(context, query):
    context = "\n".join(context)

    system_prompt = (
        "You are an expert assistant. Answer only based on the provided context. "
        "If the answer is not found, say 'No information available'."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\nQuestion: {query}"}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


def query_document():
    global index, chunks

    if not os.path.exists(INDEX_FILE_PATH):
        print("Document index not found. Use option 1 to add documents.")
        return

    # Load FAISS index and chunks
    index = faiss.read_index(INDEX_FILE_PATH)
    load_chunks()

    query = input("Enter your question: ").strip()
    query_embedding = openai.embeddings.create(model=EMBED_MODEL, input=query)
    query_vector = np.array([e.embedding for e in query_embedding.data]).astype("float32")

    print (f"query_vector : {query_vector}")

    top_indices = search_faiss_index(query_vector, index)
    print (f"top_indices : {top_indices} ")

    context = [chunks[i] for i in top_indices if i < len(chunks)]
    print (context)

    # context = []
    # print (chunks)
    # print (len(chunks))
    # for i in top_indices:
    #     print (i)        
    #     if i < len(chunks):
    #         print (chunks[i])
    #         context.append(chunks[i])


    answer = ask_gpt4(context, query)
    print(f"\nAnswer for: {query}\n{answer}\n")


def delete_document():
    # Todo
    return


def main():
    while True:
        print("\nSelect an Option:")
        print("1. Add Document to FAISS Index")
        print("2. Query Document")
        print("3. Delete Document (not implemented)")
        print("4. Exit")

        choice = input("Please select an option (1/2/3/4): ").strip()

        if choice == "1":
            add_document()
        elif choice == "2":
            query_document()
        elif choice == "3":
            delete_document()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()