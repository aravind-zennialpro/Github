from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import json

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")

# Add padding token
tokenizer.pad_token = tokenizer.eos_token
head_model.pad_token_id = head_model.config.eos_token_id

# Context and question
context = (
    "India and the United States recently agreed to remove certain tariffs that were imposed during a trade dispute. "
    "The agreement is expected to benefit key sectors such as agriculture, electronics, and manufacturing. "
    "Both governments stated that this step would strengthen economic cooperation and market access."
)

question = "What sectors will benefit from the tariff removal?"

prompt = f"\nContext: {context} \n\nQuestion: {question} \nAnswer:"

# Generate 3 answers
input_ids = tokenizer.encode(prompt, return_tensors="pt")
output_ids = head_model.generate(input_ids, max_length=100, do_sample=True, num_return_sequences=3, temperature=0.8)

# Process outputs
all_results = []

for i, output in enumerate(output_ids):
    full_text = tokenizer.decode(output, skip_special_tokens=True)

    # Extract Q and A
    q_start = full_text.find("Question")
    a_start = full_text.find("Answer")

    question_text = full_text[q_start:a_start].strip() if q_start != -1 and a_start != -1 else question
    answer_text = full_text[a_start:].strip() if a_start != -1 else full_text

    all_results.append({
        "id": i,
        "question": question_text,
        "answer": answer_text
    })

# Save to JSON
with open("qa_outputs.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)