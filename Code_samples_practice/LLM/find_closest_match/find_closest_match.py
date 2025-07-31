from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F
import json

query = "I enjoy learning Python"
candidates = [
    "Python is a powerful language",
    "Bananas are rich is potassium",
    "Studying Python is enjoyable",
    "The weather is nice today",
    "I love Programing in Java"
]

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
model.eval()
model.to("cpu")  # Ensure model runs on CPU

def get_mean_embeddings(input_text):
    tokens = tokenizer(input_text, return_tensors="pt").to("cpu")
    with torch.no_grad():
        model_output = model(**tokens)
        full_embeddings = model_output.last_hidden_state
        mean_embeddings = full_embeddings.mean(dim=1).float()
        return mean_embeddings

query_embedding = get_mean_embeddings(query)

results = []
for candidate in candidates:
    mean_embedding = get_mean_embeddings(candidate)
    score = F.cosine_similarity(query_embedding, mean_embedding, dim=1).item()
    results.append((candidate, score))

results.sort(key=lambda x: x[1], reverse=True)

print(f"\nQuery is : {query}\n")
for candidate, score in results:
    print(f"{score:.4f} → {candidate}")
    
# Save output to a JSON file
output_data = { "query": query, "results": 
    [ {"sentence": candidate, "similarity": score}
        for candidate, score in results
    ]
}

with open("similarity_results.json", "w") as f:
    json.dump(output_data, f, indent=4)
