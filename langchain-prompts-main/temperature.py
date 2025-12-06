from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4', temperature=1.5)
# Temperature value = 0.0 to 2.0
# 0 gives the most deterministic result i.e. for every run we will get the same result
# 2 gives the most creative result
# so it is crucial to set the temperature value, as it is trade off between creativity and determinism
result = model.invoke("Write a 5 line poem on cricket")

print(result.content)