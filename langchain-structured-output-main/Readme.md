# Structured Output in LangChain

## What is Structured Output?

Structured output refers to the practice of having language models generate responses in a well-defined data format (e.g., JSON) rather than free-format text. This makes the model output easier to parse and work with programmatically.

---

## Why We Need Structured Output

1. **Data Extraction** - Extract specific information in a consistent format
2. **API Building** - Create reliable APIs with predictable response structures
3. **Agents** - Enable AI agents to interact with structured data and tools

---

## Ways to Get Structured Output

### Method 1: LLMs with Native Structured Output Support

Some LLMs can generate structured output natively using the `with_structured_output()` function.

**Requirements:**
- Define the data format using:
  - TypedDict
  - Pydantic
  - JSON Schema
- Internal prompting happens automatically

### Method 2: Using Output Parsers

For LLMs that don't support native structured output, use output parsers to format the response.

---

## Data Format Options

### TypedDict

TypedDict is a way to define a dictionary in Python where you specify what keys and values should exist.

**Purpose:**
- Tells Python what keys are required and what types of values they should have
- Provides type hints for better coding experience
- **Does NOT validate data at runtime** - it's just for type representation

**Use Case:**
- Use TypedDict to define the structure of expected LLM responses
- For actual data validation, use Pydantic instead

**Example:**
```python
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    email: str
```

---

### Pydantic

Pydantic is a data validation and parsing library for Python. It ensures that the data you work with is correct, structured, and type-safe.

**Key Features:**
- **Runtime validation** - Throws errors for invalid data (e.g., "Input should be a valid string")
- **Default values** - Set fallback values for fields
- **Optional fields** - Mark fields as not required
- **Type coercion** - Automatic type conversion when possible
- **Built-in validation** - Validate data against constraints
- **Field function** - Define default values, constraints, and descriptions
- **Returns Pydantic objects** - Easily convert to JSON or dictionary

**Example:**
```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(gt=0, description="Person's age")
    email: str = Field(default="no-email@example.com")
```

**Benefits:**
- Strong runtime validation
- Clear error messages
- Easy serialization to JSON/dict
- Rich constraint system

---

### JSON Schema

JSON Schema is a language-agnostic format for defining data structures.

**When to Use:**
- Working with multiple programming languages
- Need a universal data format specification
- Integrating with systems that expect JSON Schema

**Example:**
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "email": {"type": "string"}
  },
  "required": ["name", "age"]
}
```

---

## Quick Comparison

| Feature | TypedDict | Pydantic | JSON Schema |
|---------|-----------|----------|-------------|
| Runtime validation | ❌ No | ✅ Yes | ✅ Yes (with validator) |
| Type hints | ✅ Yes | ✅ Yes | ❌ No |
| Default values | ❌ No | ✅ Yes | ✅ Yes |
| Cross-language | ❌ No | ❌ No | ✅ Yes |
| Constraints | ❌ No | ✅ Yes | ✅ Yes |

---

## Best Practices

1. **Use TypedDict** for simple type hints without validation needs
2. **Use Pydantic** when you need runtime validation and rich features
3. **Use JSON Schema** for cross-language compatibility
4. Always validate LLM outputs before using them in production
5. Provide clear field descriptions to help the LLM generate correct structures