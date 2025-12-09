# The use of TypeDict or Pydantic in structured output is to give output from llm model in structured format which could be in json format which I can directly feed to further use case like a wed developer want output in json format and he will thank you for that we use pydantic or typedict

# By default llm model are so clever that they can understand all key meaning and generate output in json format. Ex: {"name":"nitish", "age":"35"} as per our Person schema the llm will generate this output.

from typing import TypedDict

class Person(TypedDict):

    name: str
    age: int

new_person: Person = {'name':'nitish', 'age':'35'}

print(new_person)