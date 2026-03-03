import tiktoken
import torch
from supplementary import GPTModel, generate_text_simple

GPT_CONFIG_500M = {
    "vocab_size": 200256,
    "context_length": 1024,
    "emb_dim": 768,
    "n_heads": 12,
    "n_layers": 12,
    "drop_rate": 0.0,
    "qkv_bias": False
}
def text_to_token_ids(text, tokenizer):
    return torch.tensor(tokenizer.encode(text)).unsqueeze(0)

def token_ids_to_text(token_ids, tokenizer):
    return tokenizer.decode(token_ids.squeeze(0).tolist())

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = GPTModel(GPT_CONFIG_500M).to(device)
model.load_state_dict(torch.load("model.pth", map_location=device))
model.eval()

start_context = "Every effort moves you"
tokenizer = tiktoken.get_encoding("o200k_base")

token_ids = generate_text_simple(
    model=model,
    idx=text_to_token_ids(start_context, tokenizer).to(device),
    max_new_tokens=10,
    context_size=GPT_CONFIG_500M["context_length"]
)
print("Output text:\n", token_ids_to_text(token_ids, tokenizer))
