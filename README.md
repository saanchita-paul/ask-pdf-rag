# Multilingual RAG System — HSC26 Bangla 1st Paper

This project implements a simple **Retrieval-Augmented Generation (RAG)** pipeline that can answer **Bangla and English** queries using content extracted from the _HSC26 Bangla 1st Paper_ book (PDF). It combines **LangChain**, **FAISS**, and **Gemini (via Google Generative AI)** to create a context-aware answer generation system.

---

##  Features

-  Answers user questions in both **Bangla** and **English**
-  Retrieves **relevant PDF chunks** using vector similarity search
-  Maintains short-term (chat history) and long-term memory (vector DB)
-  REST API using FastAPI
-  Grounded, extractive answers only (no hallucination)
-  Evaluation matrix for relevance and groundedness

##  Project Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-  Python 3.8 or newer
-  Google API Key (with Gemini access via [Google AI Studio](https://aistudio.google.com/app/apikey))


###  Step 1: Clone the Repository

```bash
https://github.com/saanchita-paul/ask-pdf-rag.git
cd ask-pdf-rag
```


### Step 2: Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

#### Create the virtual environment
```bash
python3 -m venv .venv
```

#### Activate the virtual environment
```bash
source .venv/bin/activate
```

### Step 3: Install Requirements
Install all the required Python packages using the requirements.txt file.

```bash
pip install -r requirements.txt
```

### Step 4: Environment Variable
Create a .env file in the root directory:

```bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"

```

### Step 5: Add the PDF Corpus
Place your PDF in the data/ directory:
```bash
data/HSC26-Bangla1st-Paper.pdf
```


### Step 6: Create Vector Index
Before you can run the API, you need to process your PDF data and create the local FAISS vector store. This is a one-time step (or to be re-run whenever your data changes).
This will create a vectorstore/ directory containing the index files. This process might take a few minutes depending on the size of your PDF file.

**Note:** If you have already received a pre-indexed vectorstore folder, you can skip this step. Simply place the entire vectorstore folder in the root directory of the project before starting the API server.
```bash
python create_index.py
```


### Step 7: Start the FastAPI Server
Once the index is created, you can start the API server.
```bash
uvicorn rag_api:app --reload
```


The server will be running at http://127.0.0.1:8000. The --reload flag will automatically restart the server if you make any changes to the code.

### Using API:

Query Example:

curl -X 'POST' \
  '[http://127.0.0.1:8000/api/query](http://127.0.0.1:8000/api/query)' \
  -H 'Content-Type: application/json' \
  -d '{
     "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
  }'

Sample Output:
{
"original_query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
"answer": "১৫ বছর"
}


### Evaluation Metrics

| Metric       | Method                                                         |
| ------------ | -------------------------------------------------------------- |
| Groundedness | Human inspection: Is the answer **present in retrieved text**? |
| Relevance    | FAISS `cosine similarity` + Gemini response match              |


### Requirements Breakdown (What Each Package Does)

**Core LLM & LangChain**
| Package                  | Purpose                                                          |
| ------------------------ | ---------------------------------------------------------------- |
| `langchain`              | Core framework to build RAG pipeline                             |
| `langchain-community`    | Document loaders (e.g., `PyPDFLoader`), vector stores, utilities |
| `langchain-google-genai` | Connects to Gemini via Google API                                |
| `sentence-transformers`  | Optional alternative for embeddings (not used in this version)   |

**Document & Vector Handling**
| Package     | Purpose                                                             |
| ----------- | ------------------------------------------------------------------- |
| `pypdf`     | Used by LangChain to load PDF content via `PyPDFLoader`             |
| `faiss-cpu` | Local in-memory vector database for similarity search               |
| `pandas`    | Optional — for CSV data or tabular content (not used directly here) |

**API & Server**
| Package             | Purpose                         |
| ------------------- | ------------------------------- |
| `fastapi`           | Builds the REST API             |
| `uvicorn[standard]` | ASGI server to run FastAPI app  |
| `python-multipart`  | Support for form-data if needed |

**Config and Logging**
| Package             | Purpose                                    |
| ------------------- | ------------------------------------------ |
| `pydantic`          | Data models for query and response schemas |
| `pydantic-settings` | Read `.env` config easily                   |
| `python-dotenv`     | Load `.env` into environment               |
