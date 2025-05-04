from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Pick your model
# Try TinyLlama first because it's lighter
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # tiny model that should load easily

# Load the tokenizer and model
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

# Inference function
def ask(question):
    inputs = tokenizer(question, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example Question
question = "What is a phishing attack in cybersecurity?"
print("\nUser Question:", question)
response = ask(question)
print("\nModel Response:", response)
