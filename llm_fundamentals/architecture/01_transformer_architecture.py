import torch.nn as nn
from supplementary import TransformerBlock, LayerNorm
import torch
import tiktoken
from importlib.metadata import version

GPT_CONFIG_500M = {
    "vocab_size": 200256,    # Vocabulary size
    "context_length": 1024,  # Context length
    "emb_dim": 768,          # Embedding dimension
    "n_heads": 12,           # Number of attention heads
    "n_layers": 12,          # Number of layers
    "drop_rate": 0.0,        # Dropout rate
    "qkv_bias": False        # Query-Key-Value bias
}


class GPTModel(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.tok_emb = nn.Embedding(cfg["vocab_size"], cfg["emb_dim"])
        self.pos_emb = nn.Embedding(cfg["context_length"], cfg["emb_dim"])
        self.drop_emb = nn.Dropout(cfg["drop_rate"])
        
        self.trf_blocks = nn.Sequential(
            *[TransformerBlock(cfg) for _ in range(cfg["n_layers"])])
        
        self.final_norm = LayerNorm(cfg["emb_dim"])
        self.out_head = nn.Linear(
            cfg["emb_dim"], cfg["vocab_size"], bias=False
        )

    def forward(self, in_idx):
        batch_size, seq_len = in_idx.shape
        tok_embeds = self.tok_emb(in_idx)
        pos_embeds = self.pos_emb(torch.arange(seq_len, device=in_idx.device))
        x = tok_embeds + pos_embeds  # Shape [batch_size, num_tokens, emb_size]
        x = self.drop_emb(x)
        x = self.trf_blocks(x)
        x = self.final_norm(x)
        logits = self.out_head(x)
        return logits


tokenizer = tiktoken.get_encoding("o200k_base")

batch = []

txt1 = "In Indian style talking, people usually speak in a expressive way, where emotions and relationships matter as much as the information itself. Conversations often start with polite greetings and small talk, like asking about family, health, and work, because in India personal connection comes first. Indians tend to use a mix of English and their mother tongue, creating “Hinglish” or other blends, and sentences may be longer and more descriptive. Respect is shown through words like ji, sir, and madam, and by using softer language instead of direct refusal. Storytelling, examples, and cultural references are common, and people may repeat points for clarity and emphasis. Overall, Indian style communication feels friendly, indirect, and relationship-focused rather than blunt and purely task-oriented."
txt2 = "Indian English communication style is polite, detailed, and focusing not only on what is said but also on how it is said. Speakers often use formal-sounding phrases like “kindly,” “please do the needful,” and “as per my understanding,” which may sound old-fashioned in other countries but are normal in India. Conversations usually begin with courteous openings and end with respectful closings, showing value for harmony and mutual respect. Indian English speakers may explain things at length, giving background and context before coming to the main point, and they often avoid saying a direct “no,” preferring softer expressions like “we will try” or “let us see.” This style reflects India’s cultural emphasis on respect, patience, and maintaining good relationships while communicating."

batch.append(torch.tensor(tokenizer.encode(txt1)))
batch.append(torch.tensor(tokenizer.encode(txt2)))
batch = torch.stack(batch, dim=0)
# print(batch)

torch.manual_seed(123)
model = GPTModel(GPT_CONFIG_500M)

out = model(batch)
# print("Input batch:\n", batch)
# print("\nOutput shape:", out.shape)
# print(out)


def generate_text_simple(model, idx, max_new_tokens, context_size):
    # idx is (batch, n_tokens) array of indices in the current context
    for _ in range(max_new_tokens):
        
        # Crop current context if it exceeds the supported context size
        # E.g., if LLM supports only 5 tokens, and the context size is 10
        # then only the last 5 tokens are used as context
        idx_cond = idx[:, -context_size:]
        
        # Get the predictions
        with torch.no_grad():
            logits = model(idx_cond)
        
        # Focus only on the last time step
        # (batch, n_tokens, vocab_size) becomes (batch, vocab_size)
        logits = logits[:, -1, :]  

        # Apply softmax to get probabilities
        probas = torch.softmax(logits, dim=-1)  # (batch, vocab_size)

        # Get the idx of the vocab entry with the highest probability value
        idx_next = torch.argmax(probas, dim=-1, keepdim=True)  # (batch, 1)

        # Append sampled index to the running sequence
        idx = torch.cat((idx, idx_next), dim=1)  # (batch, n_tokens+1)

    return idx


model.eval(); 


start_context = "Hahahah"

encoded = tokenizer.encode(start_context)
print("encoded:", encoded)
encoded_tensor = torch.tensor(encoded).unsqueeze(0)
# print("encoded_tensor.shape:", encoded_tensor.shape)
out = generate_text_simple(
    model=model,
    idx=encoded_tensor, 
    max_new_tokens=20, 
    context_size=GPT_CONFIG_500M["context_length"]
)
# print("Output:", out)
# print("Output length:", len(out[0]))
decoded_text = tokenizer.decode(out.squeeze(0).tolist())
print(decoded_text)
