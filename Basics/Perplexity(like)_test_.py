from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama

search = DuckDuckGoSearchRun()

llm = ChatOllama(
    model="Your AI Model",
    temperature=0.2
)

query = "what is the Date and time now in india "

results = search.run(query)

prompt = f"""
Answer the question using the search results below.
Cite sources clearly.

Search Results:
{results}

Question: {query}
"""

response = llm.invoke(prompt)
print(response.content)
