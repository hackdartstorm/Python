from litgpt import LLM
llm = LLM.load("Qwen/Qwen3-1.7B")
llm.generate("What do Llamas eat?")
result = llm.generate("What do Llamas eat?", stream=True, max_new_tokens=200)
for e in result:
    print(e, end="", flush=True)
    