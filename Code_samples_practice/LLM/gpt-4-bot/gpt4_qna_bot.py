import os
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

index = None
chunks = []

def embed_chunks (chunks):
    embeddings = openai.embeddings.create(model=EMBED_MODEL, input = chunks)
    vectors = np.array([e.embedding for e in embeddings.data]).astype("float32")
    return vectors


def chunk_text(text):
    words = text.split() # 5000
    return [ " ".join(words[i: i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE )]


def extract_text_from_pdf(pdf_path):
    pages = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text() for page in pages])
    return full_text


def add_document():
    # Assume : Vonna Graduated in 2023. From a Collage in Hyderabad. He is a Expert Java Developer
    global index, chunks

    pdf_path = input("Enter path of PDF file : ").strip()
    if not os.path.exists(pdf_path):
        print (f"File not found on location {pdf_path}")
        return
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print ("Not content found. Try another PDF file")
        return    

    chunks = chunk_text (text)
    vectors = embed_chunks (chunks)

    if not os.path.exists (INDEX_FILE_PATH):
        index = faiss.IndexFlatL2(vectors.shape[1]) # Create a In Memory Index
    else:
        index = faiss.read_index(INDEX_FILE_PATH)    
    
    index.add(vectors)
    faiss.write_index(index, INDEX_FILE_PATH)
    print ("Document was indexed successfully")

def search_faiss_index(query_vector, index):
    """
    Compare the input from User with the data in faiss Index
    """
    distance, indices =  index.search(query_vector, 5)
    return indices[0]

def ask_gpt4(context, query):
    context = "\n".join(context)

    system_prompt = (
        "You are an expert assistant. Anwer only based on the provided context,"
        "If the answer is not found then say 'No information available'"
    )

    messages = [
        {"role" : "system", "content" : system_prompt},
        {"role" : "user", "content" : f"Context: \n {context}\n Question: {query}"}
    ]

    response = openai.chat.completions.create(
        model = "gpt-4",
        messages = messages, 
        temperature = 0.2
    )
    return response.choices[0].message.content.strip()

def query_document():  
    global index, chunks

    if not os.path.exists(INDEX_FILE_PATH):
        print ("Document index does not exists please option 1 to create.")
    else:
        index = faiss.read_index(INDEX_FILE_PATH)

    query = input ("Please enter your query or question to search in Index : ")
    query_embedding = openai.embeddings.create(model=EMBED_MODEL, input = query)
    query_vectors = np.array([e.embedding for e in query_embedding.data]).astype("float32")
    
    print (query_vectors)
    top_indices = search_faiss_index (query_vectors, index)
    context = [chunks[i] for i in top_indices]
    answer = ask_gpt4(context, query)
    print (f"\nAnswer for :  {query} is : \n {answer} ")

def delete_document():
    return True

def main():
    while True:
        print ("\nSelect an Option : ")
        print ("1. Add Document to FAISS Index")
        print ("2. Query Document")
        print ("3. Delete Document")
        print ("4. Exit")
        choice = input ("Please select an option (1/2/3/4) :").strip()

        if choice == "1": 
            add_document()
        elif choice == "2": 
            query_document()
        elif choice == "3":
            delete_document()            
        elif choice == "4":
            print ("Goodbye.... See you again!")
            break
        else:
            print ("Incorrect choice. Please try again")           


if __name__ == "__main__":
    main()