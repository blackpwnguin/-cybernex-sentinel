import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load your corpus
corpus_file = "./cyber_corpus.jsonl"
with open(corpus_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

documents = []
metadata = []

for line in lines:
    entry = json.loads(line)
    documents.append(entry["content"])
    metadata.append(entry["title"])  # Save the title to match later

# Load an embedding model
print("Loading embedding model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight + fast

# Embed all documents
print("Embedding documents...")
embeddings = embedder.encode(documents, show_progress_bar=True)

# Create FAISS index
d = embeddings.shape[1]  # Dimension
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings).astype('float32'))

# Save index and metadata
faiss.write_index(index, "cyber_index.faiss")

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f)

print(f"✅ Built FAISS index with {len(documents)} documents")
