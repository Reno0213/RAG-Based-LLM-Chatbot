# setup.py
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os
import pandas as pd
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
RAG_PINECONE_API_KEY = os.getenv("RAG_PINECONE_API_KEY")

pc = Pinecone(api_key=RAG_PINECONE_API_KEY)
index_name = "lore-bot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        vector_type="dense",
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        deletion_protection="disabled",
        tags={"environment": "development"}
    )

# Load and clean dataset
df = pd.read_csv('../data/league_lore_df.csv')
dataset = df.drop('Unnamed: 4', axis=1)

# Extract only Zyra's row
testSet = dataset.iloc[163:]  # Index 163 is Zyra

# Prepare chunker and embedder
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
text_splitter = SemanticChunker(embedding_model)
index = pc.Index(index_name)

# Upsert Zyra chunks
unique_id = 0
for _, row in testSet.iterrows():
    chunks = text_splitter.split_text(row['Lore'])
    for chunk in chunks:
        vector = embedding_model.embed_documents([chunk])
        metadata = {
            "champion": row['Champion'],
            "region": row['Region'],
            "link": row['Link'],
            "lore": chunk
        }
        unique_id += 1
        index.upsert(vectors=[{"id": str(unique_id), "values": vector[0], "metadata": metadata}])

print("Setup complete.")
