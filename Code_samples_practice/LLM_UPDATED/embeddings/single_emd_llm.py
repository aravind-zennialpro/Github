
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GOOGLE_API_KEY)
print(embeddings.embed_query("Hello, world!"))
