import os
import json

# Folder containing .txt files
corpus_folder = "./corpus"
# Output file to save JSONL
output_file = "./cyber_corpus.jsonl"

entries = []

# Loop over every .txt file in corpus
for filename in os.listdir(corpus_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(corpus_folder, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()
            entries.append({
                "title": filename.replace(".txt", "").replace("_", " ").title(),
                "content": text.strip()
            })

# Save as JSONL (one JSON object per line)
with open(output_file, "w", encoding="utf-8") as f:
    for entry in entries:
        f.write(json.dumps(entry) + "\n")

print(f"✅ Saved {len(entries)} entries to {output_file}")
