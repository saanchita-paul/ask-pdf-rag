import os
import time
from pydantic_settings import BaseSettings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DATA_PATH = "data/HSC26-Bangla1st-Paper.pdf"
DB_FAISS_PATH = "vectorstore/db_faiss"

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    class Config:
        env_file = ".env"

settings = Settings()
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

def create_vector_db():
    print(f"Loading PDF from {DATA_PATH}...")
    loader = PyPDFLoader(DATA_PATH)
    pages = loader.load()

    print("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "।", ".", " ", ""]
    )
    documents = splitter.split_documents(pages)

    if not documents:
        raise ValueError("PDF file is empty or could not be loaded.")

    print("Initializing Google Generative AI embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    print(f"Processing {len(documents)} chunks in batches...")

    batch_size = 100
    db = None

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        print(f"  - Processing batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size}...")

        if db is None:
            db = FAISS.from_documents(batch_docs, embeddings)
        else:
            db.add_documents(batch_docs)

        time.sleep(1)  # to avoid rate limits

    print(f"Saving FAISS vector store to {DB_FAISS_PATH}...")
    db.save_local(DB_FAISS_PATH)
    print("✅ Vector store created successfully!")

if __name__ == "__main__":
    if os.path.exists(DB_FAISS_PATH):
        print(f"Vector store already exists at {DB_FAISS_PATH}. Skipping creation.")
    else:
        create_vector_db()
