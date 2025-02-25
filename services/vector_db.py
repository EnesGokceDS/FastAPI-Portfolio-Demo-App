# services/vector_db.py
import os
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths for your CSV and FAISS index
DATA_CSV_PATH = "data/amazon_50k_reviews.csv"
INDEX_PATH = "faiss_index.index"

# Load your CSV file (adjust the path if necessary)
data = pd.read_csv(DATA_CSV_PATH)

# Create a combined text field using 'title' and 'text'
data['combined'] = data['title'].fillna('') + ". " + data['text'].fillna('')

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load or create the FAISS index
if os.path.exists(INDEX_PATH):
    print("Loading FAISS index from disk.")
    index = faiss.read_index(INDEX_PATH)
else:
    print("FAISS index not found, creating new index.")
    # Compute embeddings for the combined text
    embeddings = model.encode(data['combined'].tolist(), convert_to_numpy=True)
    # Normalize embeddings so that cosine similarity equals the inner product
    faiss.normalize_L2(embeddings)
    # Build a FAISS index using inner product (cosine similarity on normalized vectors)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    # Save the index to disk for future use
    faiss.write_index(index, INDEX_PATH)

def retrieve_context(query: str, max_rows: int = 100, similarity_threshold: float = 0.5) -> str:
    """
    Retrieve up to `max_rows` rows from the vector database that have at least
    `similarity_threshold` cosine similarity with the query.
    """
    # Compute query embedding and normalize it
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)
    
    # Search the FAISS index
    distances, indices = index.search(query_embedding, max_rows)
    
    # Filter out results below the similarity threshold
    relevant_indices = [i for i, sim in zip(indices[0], distances[0]) if sim >= similarity_threshold]
    if not relevant_indices:
        return ""
    
    # Retrieve the rows and combine them into a single context string
    context_rows = data.iloc[relevant_indices]
    combined_context = "\n".join(context_rows['combined'].tolist())
    return combined_context