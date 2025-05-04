import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load FAISS index and metadata
index = faiss.read_index("cyber_index.faiss")
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load the language model
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

def get_answer(question):
    # Encode the question
    question_embedding = embedder.encode([question])
    
    # Search FAISS index
    D, I = index.search(np.array(question_embedding).astype('float32'), k=1)
    best_match_idx = I[0][0]
    
    # Retrieve metadata
    context = metadata[best_match_idx]

    # Prepare prompt
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"

    # Encode and generate
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output = model.generate(input_ids, max_new_tokens=200)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    return answer
