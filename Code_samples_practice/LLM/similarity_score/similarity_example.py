from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F
import json

# Defining model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

def get_mean_embedding (input_text):
    tokens = tokenizer(input_text, return_tensors="pt")

    with torch.no_grad():
        outputs = model (**tokens)
    
    full_embeddings = outputs.last_hidden_state
    mean_embeddings = full_embeddings.mean(dim=1)
    return mean_embeddings   


sentence1 = "I enjoy learning Python"
sentence2 = "I will play everyday"

first_sentence_embedding = get_mean_embedding(sentence1)
second_sentence_embedding = get_mean_embedding(sentence2)

similarity = F.cosine_similarity (first_sentence_embedding,second_sentence_embedding).item()

print  (f"Sentence1 : {sentence1} ")
print  (f"Sentence2 : {sentence2} ")
output =  (f"Cosine Similarity : {similarity:.4f} (1 = Very Similar, 0 = different ) ")
print(output)
#saving output in json
with open("similarity_score.json", "w") as f:
    json.dump(output, f, indent=4)