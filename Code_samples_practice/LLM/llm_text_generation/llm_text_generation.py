from transformers import GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
import torch
import json

prompt = "In Future AI Agents will TakeOver?"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")


input_ids = tokenizer.encode (prompt, return_tensors ="pt")

output_ids =  head_model.generate(input_ids, max_length=500, do_sample=True)

generated_text = tokenizer.decode(output_ids[0], skip_special_tokens = True)


output =   (f"\n {prompt} \n\n Generated Text : {generated_text}")

print(output)

#saving output in json
with open("llm_text_generation.json", "w", encoding="utf-8") as f:
    f.write(output)