# Prompt Template Guide

## Overview

This guide explains when and how to use `PromptTemplate` and `ChatPromptTemplate` in LangChain for building effective prompt structures.

---

## PromptTemplate

### When to Use
- Basic, single-turn interactions with typical Large Language Models (LLMs)
- Models that accept a continuous string prompt (text-in, text-out)
- Simple tasks without conversation history or role management

### Structure
A single string template with input variables.

**Example:**
```python
from langchain.prompts import PromptTemplate

template = "Tell me a joke about {topic}"
prompt = PromptTemplate(template=template, input_variables=["topic"])
```

### Use Cases
- Single prompts
- Simple text generation tasks
- Question answering without context
- Basic text transformation or analysis

---

## ChatPromptTemplate

### When to Use
- Conversational AI and chatbots
- Multi-turn contexts requiring conversation history
- Explicit control over message roles (System, Human, AI)
- Chat-optimized models (message-in, message-out)

### Structure
A sequence of `Message` templates that form a structured conversation history with different roles:
- **System**: Instructions or context for the AI
- **Human**: User messages
- **AI**: Assistant responses

**Example:**
```python
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that specializes in {domain}."),
    ("human", "Hello, how are you?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}")
])
```

### Use Cases
- Chatbots with personality and context
- Multi-turn dialogue systems
- Applications requiring role-based message management
- Maintaining conversation history

---

## MessagesPlaceholder

### What It Is
A special placeholder that allows you to inject a list of messages dynamically into a chat prompt template at a specific position.

### When to Use
- Maintaining conversation history
- Dynamically inserting past messages
- Building chat applications with memory

**Example:**
```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_input}")
])
```

This allows you to pass a list of previous messages through the `chat_history` variable, enabling the model to reference past interactions.

---

## Key Differences at a Glance

| Feature | PromptTemplate | ChatPromptTemplate |
|---------|---------------|-------------------|
| **Model Type** | Standard LLMs (text-in, text-out) | Chat Models (message-in, message-out) |
| **Input Format** | Single string with variables | List of messages with roles (System, Human, AI) |
| **Use Cases** | Single prompts, simple tasks | Chatbots, multi-turn dialogue, context management |
| **Structure** | Plain text template | Structured message sequence |
| **Conversation History** | Not supported | Supported via MessagesPlaceholder |

---

## Quick Decision Guide

**Use `PromptTemplate` if:**
- ✓ You have a simple, one-off prompt
- ✓ You don't need conversation history
- ✓ You're using a standard text-completion LLM

**Use `ChatPromptTemplate` if:**
- ✓ You're building a conversational interface
- ✓ You need to maintain context across turns
- ✓ You want explicit role management (system, human, AI)
- ✓ You're using a chat-optimized model (GPT-4, Claude, etc.)

---

## Best Practices

1. **Start Simple**: Use `PromptTemplate` for prototyping and simple use cases
2. **Scale to Chat**: Move to `ChatPromptTemplate` when adding conversational features
3. **Use System Messages**: Leverage system messages in `ChatPromptTemplate` to set behavior and constraints
4. **Manage History**: Use `MessagesPlaceholder` for dynamic conversation history injection
5. **Test Both**: Different models may perform better with different prompt structures