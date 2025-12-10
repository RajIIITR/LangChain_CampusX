# LangChain Output Parsers Guide

## Overview

Output parsers in LangChain help convert LLM text responses into structured data formats. This guide covers the three most popular output parsers and when to use each one.

---

## Available Output Parsers

### 1. PydanticOutputParser

**Description:**  
Uses Pydantic models for strict data validation and type conversion.

**Returns:** Pydantic objects

**Best For:**
- Production applications
- Critical applications requiring strong data integrity
- Automatic type conversion needs
- Complex nested data models
- When you need runtime validation
- Applications where data correctness is crucial

**Key Features:**
- ✅ Strong runtime validation
- ✅ Automatic type coercion
- ✅ Support for nested models
- ✅ Rich constraint system
- ✅ Clear error messages
- ✅ Easy serialization (to dict/JSON)

**Example Use Cases:**
- E-commerce product data extraction
- Financial data processing
- Medical records parsing
- Legal document analysis
- Any mission-critical data extraction

**Example:**
```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(gt=0, description="Product price")
    in_stock: bool = Field(description="Availability status")

parser = PydanticOutputParser(pydantic_object=Product)
```

---

### 2. JsonOutputParser

**Description:**  
Lightweight parser that converts LLM output to Python dictionaries with optional JSON schema validation.

**Returns:** Python `dict`

**Best For:**
- General-purpose applications
- API development
- Quick JSON parsing needs
- Lightweight applications
- When you want flexibility without heavy validation
- Rapid prototyping with some validation

**Key Features:**
- ✅ Fast and lightweight
- ✅ Returns standard Python dict
- ✅ Optional schema validation
- ✅ Easy to work with
- ✅ Minimal overhead
- ✅ Good for APIs

**Example Use Cases:**
- REST API responses
- General data extraction
- Log parsing
- Configuration management
- Dashboard data feeds

**Example:**
```python
from langchain.output_parsers import JsonOutputParser

parser = JsonOutputParser()
# Returns a standard Python dictionary
```

---

### 3. StructuredOutputParser

**Description:**  
Simple parser using `ResponseSchema` for basic, predefined schemas without rigorous type checking.

**Returns:** Python `dict`

**Best For:**
- Prototyping and experimentation
- Simple scenarios
- Basic schema requirements
- When you don't need strict validation
- Quick demos and MVPs
- Learning and testing

**Key Features:**
- ✅ Simple to set up
- ✅ Uses ResponseSchema for definition
- ✅ Good for basic use cases
- ✅ Minimal configuration
- ⚠️ Limited validation
- ⚠️ No automatic type conversion

**Example Use Cases:**
- Quick prototypes
- Simple data extraction tasks
- Educational projects
- Basic automation scripts
- Early-stage development

**Example:**
```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

response_schemas = [
    ResponseSchema(name="name", description="The person's name"),
    ResponseSchema(name="age", description="The person's age")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
```

---

## Quick Comparison Table

| Feature | PydanticOutputParser | JsonOutputParser | StructuredOutputParser |
|---------|---------------------|------------------|------------------------|
| **Return Type** | Pydantic object | dict | dict |
| **Validation Strength** | Strong | Optional | Basic |
| **Type Conversion** | Automatic | Manual | Manual |
| **Nested Models** | ✅ Yes | ⚠️ Limited | ❌ No |
| **Performance** | Moderate | Fast | Fast |
| **Complexity** | Higher | Low | Low |
| **Best For** | Production | General use | Prototyping |
| **Error Handling** | Detailed | Basic | Basic |
| **Learning Curve** | Steeper | Easy | Easy |

---

## Decision Flow Chart

```
Need structured output?
│
├─ Is this production/critical? 
│  └─ YES → Use PydanticOutputParser
│
├─ Need quick API/general parsing?
│  └─ YES → Use JsonOutputParser
│
└─ Just prototyping/simple task?
   └─ YES → Use StructuredOutputParser
```

---

## Best Practices

### When to Choose Each Parser

**Choose PydanticOutputParser when:**
- Building production systems
- Data integrity is critical
- You need nested object validation
- Working with complex data structures
- Type safety is a requirement
- You need automatic type conversion

**Choose JsonOutputParser when:**
- Building APIs
- Need standard Python dicts
- Want lightweight parsing
- Performance is important
- Flexibility is valued over strict validation
- Working with simple to moderate structures

**Choose StructuredOutputParser when:**
- In prototyping phase
- Building simple demos
- Learning LangChain
- Don't need strict validation
- Working with flat, simple structures
- Speed of development is priority

---

## Migration Path

**Typical development progression:**

1. **Start:** StructuredOutputParser (rapid prototyping)
2. **Develop:** JsonOutputParser (testing and refinement)
3. **Deploy:** PydanticOutputParser (production-ready)

---

## Code Examples

### PydanticOutputParser - Full Example
```python
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator

class UserProfile(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(gt=0, lt=150, description="User's age")
    email: str = Field(description="User's email address")
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

parser = PydanticOutputParser(pydantic_object=UserProfile)

prompt = PromptTemplate(
    template="Extract user information:\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

### JsonOutputParser - Full Example
```python
from langchain.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

### StructuredOutputParser - Full Example
```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

response_schemas = [
    ResponseSchema(name="answer", description="The answer to the question"),
    ResponseSchema(name="source", description="Source of the information")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

prompt = PromptTemplate(
    template="Answer the question.\n{format_instructions}\n{question}",
    input_variables=["question"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

---

## Summary

- **PydanticOutputParser**: Maximum validation, production-ready, type-safe
- **JsonOutputParser**: Balanced approach, flexible, API-friendly
- **StructuredOutputParser**: Simplest option, quick setup, prototyping

Choose based on your project's maturity, validation needs, and complexity requirements.