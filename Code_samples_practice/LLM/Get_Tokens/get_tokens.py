from transformers import GPT2Tokenizer
import json
# Due to using of gpt2 it was pretrained model so we dont get accurate results.
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokens = tokenizer.tokenize("My Name is Aravind Puttapaka")
print(tokens)
# saving output is json
with open("tokens_output.json", "w", encoding="utf-8") as f:
    json.dump(tokens, f, indent=4, ensure_ascii=False)