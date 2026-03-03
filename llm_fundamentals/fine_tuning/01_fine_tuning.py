import json

file_path = "../../WEIGHT-LOADING/instruction-data.json"

with open(file_path, "r") as file:
    data = json.load(file)
print("Number of entries:", len(data))
train_portion = int(len(data) * 0.85)  # 85% for training
test_portion = int(len(data) * 0.15)    # 15% for testing

train_data = data[:train_portion]
test_data = data[train_portion:]
print("Training set length:", len(train_data))
print("Test set length:", len(test_data))
with open("train.json", "w") as json_file:
    json.dump(train_data, json_file, indent=4)
    
with open("test.json", "w") as json_file:
    json.dump(test_data, json_file, indent=4)


def format_input(entry):
    instruction_text = (
        f"Below is an instruction that describes a task. "
        f"Write a response that appropriately completes the request."
        f"\n\n### Instruction:\n{entry['instruction']}"
    )

    input_text = f"\n\n### Input:\n{entry['input']}" if entry["input"] else ""

    return instruction_text + input_text

print(format_input(test_data[0]))
from litgpt import LLM

llm = LLM.load("Qwen/Qwen3-1.7B")
from tqdm import tqdm

for i in tqdm(range(len(test_data))):
    response = llm.generate(test_data[i])
    test_data[i]["base_model"] = response
