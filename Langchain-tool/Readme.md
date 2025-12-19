# LangChain Tools Guide

A comprehensive guide to understanding and working with tools in LangChain, covering creation, binding, calling, execution, and dependency injection.

## Table of Contents
- [Overview](#overview)
- [Tool Creation](#tool-creation)
- [Tool Binding](#tool-binding)
- [Tool Calling](#tool-calling)
- [Tool Execution](#tool-execution)
- [InjectedToolArg](#injectedtoolarg)
- [About the Requests Module](#about-the-requests-module)
- [Best Practices](#best-practices)

## Overview

Tools in LangChain are interfaces that allow Language Models (LLMs) to interact with external systems, APIs, databases, and other resources. They extend the capabilities of LLMs beyond text generation to perform actions in the real world.

## Tool Creation

LangChain provides multiple ways to create tools:

### 1. Using the `@tool` Decorator

The simplest way to create a tool is using the `@tool` decorator:

```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b
```

### 2. Using the `Tool` Class

For more control, you can use the `Tool` class directly:

```python
from langchain.tools import Tool

def search_function(query: str) -> str:
    # Your search logic here
    return f"Results for: {query}"

search_tool = Tool(
    name="Search",
    func=search_function,
    description="Useful for searching information on the internet"
)
```

### 3. Using `StructuredTool`

For tools with multiple parameters and complex input schemas:

```python
from langchain.tools import StructuredTool

def complex_calculation(x: int, y: int, operation: str) -> int:
    """Perform complex calculations."""
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y
    return 0

calc_tool = StructuredTool.from_function(
    func=complex_calculation,
    name="Calculator",
    description="Performs mathematical operations"
)
```

### 4. Subclassing `BaseTool`

For advanced use cases with custom validation and error handling:

```python
from langchain.tools import BaseTool
from pydantic import Field

class CustomSearchTool(BaseTool):
    name: str = "custom_search"
    description: str = "Searches for information"
    api_key: str = Field(default="your-api-key")
    
    def _run(self, query: str) -> str:
        """Execute the tool."""
        # Your implementation here
        return f"Search results for: {query}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        raise NotImplementedError("Async not implemented")
```

## Tool Binding

Tool binding is the process of making tools available to an LLM. This tells the model what tools exist and how to use them.

### Basic Binding

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Create an LLM instance
llm = ChatOpenAI(model="gpt-4")

# Bind tools to the LLM
llm_with_tools = llm.bind_tools([get_weather])
```

### Multiple Tools Binding

```python
@tool
def calculator(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

@tool
def get_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# Bind multiple tools
llm_with_tools = llm.bind_tools([get_weather, calculator, get_time])
```

## Tool Calling

**Important Note:** Tool calling refers to the LLM's decision-making process where it determines which tool(s) to invoke and with what parameters. The LLM does NOT actually execute the tools—it only suggests which tools should be called and provides the reasoning for that choice.

This separation exists to prevent incorrect tool execution. If the LLM directly executed tools, a wrong tool call could lead to unintended consequences, incorrect results, or even harmful actions. By having the LLM only suggest tool calls, developers maintain control over the actual execution.

### How Tool Calling Works

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

llm = ChatOpenAI(model="gpt-4")
llm_with_tools = llm.bind_tools([add_numbers])

# The LLM will suggest using the tool, not execute it
response = llm_with_tools.invoke("What is 25 plus 17?")

# Response contains tool call suggestions
print(response.tool_calls)
# Output: [{'name': 'add_numbers', 'args': {'a': 25, 'b': 17}, 'id': '...'}]
```

### Understanding the Response

The LLM's response includes:
- **name**: The tool it recommends calling
- **args**: The parameters to pass to the tool
- **id**: A unique identifier for tracking the tool call
- **reasoning** (implicit): The LLM has determined this tool is appropriate for the query

## Tool Execution

Tool execution is the actual process of running the tool with the parameters suggested by the LLM. This happens separately from tool calling and is typically controlled by the developer or an agent.

### Manual Tool Execution

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y

llm = ChatOpenAI(model="gpt-4")
llm_with_tools = llm.bind_tools([multiply])

# Step 1: LLM suggests tool call
response = llm_with_tools.invoke("Calculate 8 times 7")

# Step 2: Extract tool call information
if response.tool_calls:
    tool_call = response.tool_calls[0]
    tool_name = tool_call['name']
    tool_args = tool_call['args']
    
    # Step 3: Manually execute the tool
    result = multiply.invoke(tool_args)
    print(f"Result: {result}")  # Output: Result: 56
```

### Agent-Based Tool Execution

Agents automatically handle the tool execution cycle:

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool

@tool
def search_database(query: str) -> str:
    """Search the database for information."""
    # Simulated database search
    return f"Database results for: {query}"

@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)

# Create tools list
tools = [search_database, calculate]

# Create LLM and prompt
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create executor that handles tool execution
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# The agent will automatically:
# 1. Call the LLM
# 2. Parse tool calls
# 3. Execute the tools
# 4. Return results to the LLM
# 5. Repeat until task is complete

result = agent_executor.invoke({"input": "Search for user data and calculate 100 * 2"})
print(result)
```

### Using ToolNode for Execution

LangGraph provides `ToolNode` for automatic tool execution in workflows:

```python
from langgraph.prebuilt import ToolNode
from langchain.tools import tool

@tool
def get_user_info(user_id: int) -> dict:
    """Retrieve user information."""
    return {"user_id": user_id, "name": "John Doe", "email": "john@example.com"}

tools = [get_user_info]
tool_node = ToolNode(tools)

# In a graph workflow, tool_node will automatically execute tools
# when it receives tool call messages from the LLM
```

## InjectedToolArg

`InjectedToolArg` (also known as `InjectionToolArg`) is a special type annotation in LangChain that allows you to inject dependencies into tool functions without requiring the LLM to provide them. This is essential when tools need access to resources like API clients, database connections, or configuration objects that the LLM shouldn't know about.

### Why Use InjectedToolArg?

When performing operations like currency conversion followed by multiplication, you need an exchange rate API client. The LLM shouldn't have to know about API keys, authentication, or client objects—it should only focus on the business logic (convert currency, then multiply). `InjectedToolArg` allows you to inject these dependencies securely.

### Example: Currency Conversion with Multiplication

```python
from langchain.tools import tool
from typing import Annotated
from langchain_core.tools import InjectedToolArg

class ExchangeRateClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        # API call to get exchange rate
        return 0.85  # Simulated rate

@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    client: Annotated[ExchangeRateClient, InjectedToolArg]
) -> float:
    """Convert amount from one currency to another."""
    rate = client.get_rate(from_currency, to_currency)
    return round(amount * rate, 2)

@tool
def multiply_amount(amount: float, multiplier: float) -> float:
    """Multiply an amount by a given multiplier."""
    return round(amount * multiplier, 2)

# Usage with Agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Initialize client with API key (injected, not seen by LLM)
exchange_client = ExchangeRateClient(api_key="secret-key")

tools = [convert_currency, multiply_amount]
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Execute with injected client
result = agent_executor.invoke(
    {"input": "Convert 100 USD to EUR, then multiply by 5"},
    config={"configurable": {"client": exchange_client}}
)
```

**Key Benefits**:
- **Security**: API keys stay out of LLM conversations
- **Efficiency**: No need to serialize/deserialize complex objects
- **Separation**: LLM focuses on logic, not implementation details

## About the Requests Module

### What is the Requests Module?

The `requests` module is a popular Python HTTP library used for making HTTP requests to web servers and APIs. It simplifies the process of sending HTTP requests and handling responses.

**Verification:** ✅ **CONFIRMED** - The requests module is indeed used for getting responses from the network (internet/web servers).

### Common Uses

```python
import requests

# GET request - retrieve data from a server
response = requests.get('https://api.example.com/data')
print(response.json())  # Parse JSON response

# POST request - send data to a server
data = {'key': 'value'}
response = requests.post('https://api.example.com/submit', json=data)

# Response properties
print(response.status_code)  # HTTP status code (200, 404, etc.)
print(response.text)         # Response body as text
print(response.headers)      # Response headers
```

### Using Requests in LangChain Tools

```python
from langchain.tools import tool
import requests

@tool
def fetch_api_data(endpoint: str) -> str:
    """Fetch data from an API endpoint."""
    try:
        response = requests.get(f"https://api.example.com/{endpoint}")
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {str(e)}"

@tool
def post_data(data: dict) -> str:
    """Send data to an API."""
    try:
        response = requests.post(
            "https://api.example.com/submit",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        return f"Data posted successfully: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error posting data: {str(e)}"
```

### Key Features of Requests Module

- **Simple API**: Easy-to-use methods for all HTTP verbs (GET, POST, PUT, DELETE, etc.)
- **Automatic encoding**: Handles URL encoding and JSON serialization automatically
- **Session support**: Maintain cookies and connection pooling across requests
- **SSL verification**: Built-in SSL certificate verification
- **Timeout handling**: Set timeouts to prevent hanging requests
- **Response handling**: Easy access to response content, headers, and status codes

### Installation

```bash
pip install requests
```

## Best Practices

1. **Clear Descriptions**: Always provide clear, descriptive docstrings for tools—the LLM uses these to understand when to use each tool.

2. **Type Hints**: Use proper type hints to help LangChain generate accurate tool schemas.

3. **Error Handling**: Implement proper error handling in tool functions to gracefully handle failures.

4. **Validation**: Validate tool execution results before passing them back to the LLM.

5. **Security**: Be cautious with tools that perform sensitive operations. Consider implementing approval workflows for critical actions. Use `InjectedToolArg` for sensitive data like API keys.

6. **Testing**: Test tools independently before integrating them with LLMs to ensure they work correctly.

## Summary

- **Tool Creation**: Define functions with the `@tool` decorator or other methods
- **Tool Binding**: Make tools available to the LLM using `bind_tools()`
- **Tool Calling**: LLM suggests which tools to use (doesn't execute them)
- **Tool Execution**: Actual execution of tools with LLM-suggested parameters
- **InjectedToolArg**: Inject dependencies like API clients without exposing them to the LLM
- **Requests Module**: Python library for HTTP requests, used to fetch data from the web/network

This separation between calling and execution provides safety, control, and flexibility in building AI applications with LangChain.