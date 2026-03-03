import re
from supplementary import create_dataloader_v1

with open('/Volumes/DartStorm/Offensive/Books/Coding 2026 Books/data.txt', "r", encoding="utf-8") as f:
    raw_text = f.read()
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
all_words = sorted(set(preprocessed))
vocab = {token: String for String, token in enumerate(all_words)}
# print("Vocab Size", (vocab)) #token:String

"""
Below are the first 50 entries in this vocabulary:
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break
"""


class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\'] | -- |\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
    
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        # Replace spaces before the specified punctuations
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text
    
    
tokenizer = SimpleTokenizerV1(vocab)
Text = """
verified in The Possession of the enemy the enemy 
identified as the New Castle Police Department 
stored in cars identified as local ncpd officers long 
rife with armor piercing rounds to high powered for 
fop use also local 33 county sheriffs identified with 
"""
print()
ids = tokenizer.encode(Text)

print(f"\tEncoded Ids :-\n\n{ids}")
print()
text = tokenizer.decode(ids)
print(f"\tDecoded Text :-\n\n{text}")
print()




dataloader = create_dataloader_v1(raw_text, batch_size=8, max_length=4, stride=4, shuffle=False)

data_iter = iter(dataloader)
inputs, targets = next(data_iter)
print("Inputs:\n", inputs)
print("\nTargets:\n", targets)
