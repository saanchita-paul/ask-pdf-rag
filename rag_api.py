from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_app import setup_rag_chain, DB_FAISS_PATH, OUTPUT_DIR
from create_index import create_vector_db
import os
import re
import json
from datetime import datetime
from typing import List, Dict
from helper import cleanup_old_logs

app = FastAPI(title="RAG API with Gemini")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
if not os.path.exists(DB_FAISS_PATH):
    raise FileNotFoundError(f"Vector store not found at {DB_FAISS_PATH}. Please contact support or try again later.")

rag_chain = setup_rag_chain()
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input schema
class QueryInput(BaseModel):
    query: str
    chat_history: List[Dict[str, str]] = []

# Output schema
class ApiResponse(BaseModel):
    original_query: str
    answer: str

@app.post("/api/query", response_model=ApiResponse)
async def ask_question(input: QueryInput):
    # Use original query directly
    response = await rag_chain.ainvoke({"input": input.query})
    answer = response.get("answer", "No answer found.")

    # Clean up logs older than 1 hour
    cleanup_old_logs(OUTPUT_DIR)

    # Save log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = re.sub(r'\W+', '_', input.query.strip())[:30]
    filename = f"{timestamp}_{safe_query}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    def custom_serializer(obj):
        try:
            return obj.__dict__
        except AttributeError:
            return str(obj)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "original_query": input.query,
        "response": response,
        "answer": answer
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=2, default=custom_serializer)

    return {
        "original_query": input.query,
        "answer": answer
    }
