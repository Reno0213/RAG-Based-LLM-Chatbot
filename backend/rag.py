from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
# from transformers import pipeline
from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"] to be specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")
templates = Jinja2Templates(directory="../frontend")

# Connect to Pinecone Index
load_dotenv()
RAG_PINECONE_API_KEY = os.getenv("RAG_PINECONE_API_KEY")
pc = Pinecone(api_key=RAG_PINECONE_API_KEY)
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
index = pc.Index("lore-bot")

def generate_response(query: str) -> str:
    # Embed the query with the same model that embeds the lore vectors
    query_vector = embedding_model.embed_query(query)

    # Retrieve the list of response vectors that are most similar to the query vector
    results = index.query(vector=query_vector, top_k=1, include_metadata=True)

    # Retrieve from Pinecone
    if not results['matches']:
        return "No relevant information found."

    return results['matches'][0]['metadata']['lore']

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/generate", response_class=HTMLResponse)
# async def post_response(request: Request, query: str = Form(...)):
#     response = generate_response(query)
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "answer": response})

class ChatQuery(BaseModel):
    query: str

@app.post("/chat")
async def chat_api(data: ChatQuery):
    response = generate_response(data.query)
    return {"response": response}