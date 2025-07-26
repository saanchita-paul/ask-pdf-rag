import os
import time
from pydantic_settings import BaseSettings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

OUTPUT_DIR = "responses"
DB_FAISS_PATH = "vectorstore/db_faiss"

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    class Config:
        env_file = ".env"

settings = Settings()
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

def setup_rag_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    prompt = ChatPromptTemplate.from_template("""


    You are an expert AI assistant that provides concise. Your goal is to provide clear and accurate answers based on the context provided.

    **Context:**
    The following context is taken from the HSC Bangla 1st Paper book. It contains literary content including events, character references, and facts from the original text.
    ```
    {context}
    ```

    **Instructions:**
    1.  Carefully analyze the user's **Question** below.
    2.  Synthesize a comprehensive answer using the information from the **Context**.
    3.  The user will ask a question in either English or Bengali.
    4.  Your goal is to extract the exact answer from the context.
    5.  Do not mention the context in your answer. Respond as if you are answering the question directly.
    6.  If the answer is a single word, provide only that word.
    7.  If the context does not contain the answer, respond with "No relevant information found."
    8.  Do NOT make up answers. Do NOT include any additional conversational text or explanations.

    ---

    **Examples:**

    **Example 1: Simple Fact Retrieval**
    * **Context:**
        `কিন্তু অনুপমের চোখে, বিশেষ করে যখন সে কল্যাণীর কথা ভাবছিল, তখন শুম্ভুনাথকেই সুপুরুষ বলা যায়। তার ব্যক্তিত্ব এবং স্থিরতা অনুপমকে মুগ্ধ করেছিল।`
    * **Question:**
        অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
    * **Answer:**
        শুম্ভুনাথ

    **Example 2: Simple Fact Retrieval**
    * **Context:**
        `কিন্তু অনুপমের চোখে, বিশেষ করে যখন সে কল্যাণীর কথা ভাবছিল, তখন শুম্ভুনাথকেই সুপুরুষ বলা যায়। তার ব্যক্তিত্ব এবং স্থিরতা অনুপমকে মুগ্ধ করেছিল।`
    * **Question:**
         কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?
    * **Answer:**
        মামাকে

    **Example 3: Simple Fact Retrieval**
    * **Context:**
        `কিন্তু অনুপমের চোখে, বিশেষ করে যখন সে কল্যাণীর কথা ভাবছিল, তখন শুম্ভুনাথকেই সুপুরুষ বলা যায়। তার ব্যক্তিত্ব এবং স্থিরতা অনুপমকে মুগ্ধ করেছিল।`
    * **Question:**
         বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
    * **Answer:**
        ১৫ বছর

    ---

    **Question:**
    {input}

    **Answer:**
    """)

    retriever = db.as_retriever(search_kwargs={"k": 20})
    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, document_chain)

