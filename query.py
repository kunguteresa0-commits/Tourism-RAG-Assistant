import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_collection("travel_documents")

groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def normalize_embeddings(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return (embeddings / norms).tolist()

def ask(question: str):
    # Convert question to embedding
    query_embedding = model.encode([question])
    query_embedding = normalize_embeddings(query_embedding)

    # Retrieve top 3 documents
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not docs:
        return "No relevant information found.", []

    context = "\n\n".join(docs)

    # Generate grounded answer
    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a tourism assistant for Kenya. Answer ONLY using the provided context. If the answer is not in the context, say you do not have enough information. Be concise and specific."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip()

    sources = list({meta["source"] for meta in metadatas})

    return answer, sources
    