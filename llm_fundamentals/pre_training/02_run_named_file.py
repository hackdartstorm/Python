import torch

# Imports from a local file
from supplementary import GPTModel
GPT_CONFIG_500M = {
    "vocab_size": 200256,
    "context_length": 1024,
    "emb_dim": 768,
    "n_heads": 12,
    "n_layers": 12,
    "drop_rate": 0.0,
    "qkv_bias": False
}

model = GPTModel(GPT_CONFIG_500M)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load("model.pth", map_location=device))
model.eval()
