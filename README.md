# PDF RAG API with Google Gemini

---

## ⚙️ Project Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   Python 3.8 or newer
-   A Google API Key with the "Generative Language API" enabled. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Step 1: Clone the Repository

First, clone the repository to your local machine.

```bash
https://github.com/saanchita-paul/ask-pdf-rag.git
cd ask-pdf-rag

Step 2: Set Up a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

Step 3: Install Dependencies
Install all the required Python packages using the requirements.txt file.

pip install -r requirements.txt


Run the vector creation script:
python create_index.py

Step 4: Configure Environment Variables
Create a file named .env in the root directory of the project. This file will securely store your Google API key.

Add your API key to the .env file as follows:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"

Step 5: Add Your Data
Place your data file named ichoose-data.csv inside the data/ folder.

Running the Application

Step 1: Create the Vector Store Index
Before you can run the API, you need to process your PDF data and create the local FAISS vector store. This is a one-time step (or to be re-run whenever your data changes). 

This will create a vectorstore/ directory containing the index files. This process might take a few minutes depending on the size of your PDF file.

Note: If you have already received a pre-indexed vectorstore folder, you can skip this step. Simply place the entire vectorstore folder in the root directory of the project before starting the API server.

Step 2: Start the FastAPI Server
Once the index is created, you can start the API server.

uvicorn rag_api:app --reload

The server will be running at http://127.0.0.1:8000. The --reload flag will automatically restart the server if you make any changes to the code.

Using API:
You can send a POST request from another terminal.

First question (no history):

curl -X 'POST' \
  '[http://127.0.0.1:8000/api/query](http://127.0.0.1:8000/api/query)' \
  -H 'Content-Type: application/json' \
  -d '{
     "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
  }'

Follow-up question:

curl -X 'POST' \
  '[http://127.0.0.1:8000/api/query](http://127.0.0.1:8000/api/query)' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "what about his phone number?",
    "chat_history": [
        {
            "role": "human",
            "content": "What is the email for participant SPARKYSTU?"
        },
        {
            "role": "ai",
            "content": "The email for participant SPARKYSTU is zulukeri@xtra.co.nz."
        }
    ]
  }'
