from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os
import pandas as pd
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

# Creating Pinecone Index
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
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
        deletion_protection="disabled",
        tags={
            "environment": "development"
        }
    )

# Formatting dataset
df = pd.read_csv('data/league_lore_df.csv')
dataset = df.drop('Unnamed: 4', axis=1)

# Create test set containing only the last champion (Zyra) entry as its entire dataset
testSet = dataset.copy()
for i in range(164):
    testSet.drop(i, inplace=True)

"""
Chunking
"""
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
text_splitter = SemanticChunker(embedding_model)

index = pc.Index("lore-bot")
unique_id = 0


"""
Upserting
"""
# Iterates through the test dataset and stores the metadata of the current row (a.k.a champion)
for _, rows in testSet.iterrows():
    link = rows['Link']
    champion  = rows['Champion']
    region = rows['Region']
    lore = rows['Lore']

    # Chunks the lore section of the champion using SemanticChunker
    chunks = text_splitter.split_text(lore)

    # Uses the same model to embed the chunks, preparing for upsert
    for c in chunks:
        vector = embedding_model.embed_documents([c])
        metadata = {
            "champion": champion,
            "region": region,
            "link": link,
            "lore": c
        }
        unique_id += 1
        index.upsert(vectors=[{"id": str(unique_id), "values": vector[0], "metadata": metadata}])

def generate_response(query: str) -> str:
    """
    Retrieval
    """
    # Query the database
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    index = pc.Index("lore-bot")

    # Embed the query with the same model that embeds the lore vectors
    query = "Who is Zyra"
    query_vector = embedding_model.embed_query(query)

    # Retrieve the list of response vectors that are most similar to the query vector
    results = index.query(vector=query_vector, top_k=1, include_metadata=True)

    # Store the lore data of each result vector into a list
    retrieved_chunks = []

    for match in results['matches']:
        retrieved_chunks.append(match['metadata']['lore'])

    return results['matches'][0]['metadata']['lore']

    context_chunks = []
    if results['matches']:
        first_vector = results['matches'][0]['metadata']['lore']
        context_chunks.append(first_vector)


    """
    Prompt Engineering
    """
    # Separate each lore chunk using \n\n so the LLM can understand where one chunk ends and where one begins

    context = "\n\n".join(retrieved_chunks)
    query = "Who is Zyra"

    prompt = f"""Answer the following question about League of Legends champion lore based on the provided context. Be accurate and concise.

    Context: {context}

    Question: {query}

    Answer:"""

    generator = pipeline("text-generation", model="BAAI/bge-base-en-v1.5", max_length=512, truncation=True)

    # Generate the answer
    response = generator(prompt, max_new_tokens=512)
    return response[0]['generated_text']

    """
    Generation
    """

    ###
    # Initialize Flan-T5 for generation (best for lore Q&A)
    # Use flan-t5-large for better quality
    # Adjust based on your character limit
    # Lower temperature for more factual responses
    ###
    generator = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",  
        max_length=300,  
        do_sample=True,
        temperature=0.3,  
        early_stopping=True
    )

    # Step 4: Generate response
    response = generator(prompt, max_length=200, num_return_sequences=1)
    return response[0]['generated_text']
