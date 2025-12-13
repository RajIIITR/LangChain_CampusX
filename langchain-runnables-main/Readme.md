# LangChain Runnable Primitives

A comprehensive guide to all runnable primitives in LangChain's Expression Language (LCEL).

## Table of Contents

- [Introduction](#introduction)
- [Core Runnable Interface](#core-runnable-interface)
- [Basic Runnable Primitives](#basic-runnable-primitives)
- [Composition Primitives](#composition-primitives)
- [Control Flow Primitives](#control-flow-primitives)
- [Advanced Primitives](#advanced-primitives)
- [Usage Examples](#usage-examples)

## Introduction

LangChain Expression Language (LCEL) provides a declarative way to compose chains through runnable primitives. All runnables implement a standard interface with methods like `invoke()`, `batch()`, `stream()`, and `ainvoke()` for async operations.

## Core Runnable Interface

Every runnable in LangChain implements these core methods:

- **invoke(input)** - Process a single input synchronously
- **ainvoke(input)** - Process a single input asynchronously
- **batch(inputs)** - Process multiple inputs in parallel
- **abatch(inputs)** - Process multiple inputs in parallel asynchronously
- **stream(input)** - Stream output for a single input
- **astream(input)** - Stream output asynchronously

## Basic Runnable Primitives

### RunnableLambda

Wraps any Python function into a runnable.

```python
from langchain_core.runnables import RunnableLambda

# Simple function wrapper
def add_prefix(text):
    return f"Processed: {text}"

runnable = RunnableLambda(add_prefix)
result = runnable.invoke("hello")  # "Processed: hello"
```

### RunnablePassthrough

Passes input through unchanged or adds additional keys to the input.

```python
from langchain_core.runnables import RunnablePassthrough

# Pass through unchanged
passthrough = RunnablePassthrough()

# Add additional keys
passthrough_with_assignment = RunnablePassthrough.assign(
    extra_field=lambda x: x["field"] * 2
)
```

### RunnableParallel

Runs multiple runnables in parallel and combines their outputs.

```python
from langchain_core.runnables import RunnableParallel, RunnableLambda

parallel = RunnableParallel(
    uppercase=RunnableLambda(lambda x: x.upper()),
    lowercase=RunnableLambda(lambda x: x.lower()),
    length=RunnableLambda(lambda x: len(x))
)

result = parallel.invoke("Hello")
# {"uppercase": "HELLO", "lowercase": "hello", "length": 5}
```

### RunnableSequence

Chains multiple runnables together sequentially (created using `|` operator).

```python
from langchain_core.runnables import RunnableLambda

step1 = RunnableLambda(lambda x: x * 2)
step2 = RunnableLambda(lambda x: x + 10)

sequence = step1 | step2
result = sequence.invoke(5)  # (5 * 2) + 10 = 20
```

## Composition Primitives

### RunnableBranch

Routes input to different runnables based on conditions.

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

branch = RunnableBranch(
    (lambda x: x < 0, RunnableLambda(lambda x: "negative")),
    (lambda x: x == 0, RunnableLambda(lambda x: "zero")),
    RunnableLambda(lambda x: "positive")  # default
)

result = branch.invoke(-5)  # "negative"
```

### RunnableMap

Maps a dictionary of runnables over the input (similar to RunnableParallel).

```python
from langchain_core.runnables import RunnableMap, RunnableLambda

runnable_map = RunnableMap({
    "doubled": RunnableLambda(lambda x: x * 2),
    "tripled": RunnableLambda(lambda x: x * 3)
})

result = runnable_map.invoke(5)
# {"doubled": 10, "tripled": 15}
```

### RunnablePick

Extracts specific keys from a dictionary output.

```python
from langchain_core.runnables import RunnablePick

# Pick single key
picker = RunnablePick("key_name")

# Pick multiple keys
picker = RunnablePick(["key1", "key2"])

result = picker.invoke({"key1": "a", "key2": "b", "key3": "c"})
# {"key1": "a", "key2": "b"}
```

## Control Flow Primitives

### RunnableRetry

Adds retry logic to any runnable.

```python
from langchain_core.runnables import RunnableLambda

def unstable_function(x):
    # Might fail sometimes
    return x

runnable = RunnableLambda(unstable_function).with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

### RunnableTimeout

Adds timeout to runnable execution.

```python
runnable = some_runnable.with_timeout(seconds=30)
```

### RunnableFallbacks

Provides fallback options if the primary runnable fails.

```python
from langchain_core.runnables import RunnableLambda

primary = RunnableLambda(lambda x: risky_operation(x))
fallback = RunnableLambda(lambda x: safe_operation(x))

with_fallback = primary.with_fallbacks([fallback])
```

## Advanced Primitives

### RunnableWithMessageHistory

Adds conversation memory/history management to a runnable.

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)
```

### RunnableBinding

Binds specific arguments or configuration to a runnable.

```python
from langchain_core.runnables import RunnableBinding

# Bind specific parameters
bound_runnable = runnable.bind(temperature=0.7, max_tokens=100)

# Bind configuration
configured = runnable.bind(stop=["\n\n"])
```

### RunnableConfig

Passes runtime configuration to runnables.

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    tags=["production"],
    metadata={"user_id": "123"},
    callbacks=[callback_handler]
)

result = runnable.invoke(input, config=config)
```

### RunnableGenerator

Creates a runnable from a generator function for streaming.

```python
from langchain_core.runnables import RunnableGenerator

def generate_stream(input):
    for i in range(input):
        yield i

streaming_runnable = RunnableGenerator(generate_stream)

for chunk in streaming_runnable.stream(5):
    print(chunk)  # 0, 1, 2, 3, 4
```

### RunnableEach

Applies a runnable to each element in a list.

```python
from langchain_core.runnables import RunnableLambda

processor = RunnableLambda(lambda x: x.upper())
each_runnable = processor.map()  # or RunnableEach(processor)

result = each_runnable.invoke(["hello", "world"])
# ["HELLO", "WORLD"]
```

## Usage Examples

### Complex Chain Example

```python
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough
)

# Create a complex processing chain
chain = (
    RunnablePassthrough.assign(
        preprocessed=RunnableLambda(lambda x: x["text"].strip())
    )
    | RunnableParallel(
        original=RunnablePassthrough(),
        analysis={
            "word_count": RunnableLambda(lambda x: len(x["preprocessed"].split())),
            "char_count": RunnableLambda(lambda x: len(x["preprocessed"])),
            "uppercase": RunnableLambda(lambda x: x["preprocessed"].upper())
        }
    )
)

result = chain.invoke({"text": "  hello world  "})
```

### Error Handling Example

```python
from langchain_core.runnables import RunnableLambda

def might_fail(x):
    if x < 0:
        raise ValueError("Negative number")
    return x * 2

safe_runnable = (
    RunnableLambda(might_fail)
    .with_retry(stop_after_attempt=3)
    .with_fallbacks([
        RunnableLambda(lambda x: 0)  # Return 0 on failure
    ])
)
```

### Conditional Processing Example

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

classifier = RunnableBranch(
    (lambda x: "error" in x.lower(), 
     RunnableLambda(lambda x: {"type": "error", "msg": x})),
    (lambda x: "warning" in x.lower(), 
     RunnableLambda(lambda x: {"type": "warning", "msg": x})),
    RunnableLambda(lambda x: {"type": "info", "msg": x})
)

result = classifier.invoke("Error: Something went wrong")
# {"type": "error", "msg": "Error: Something went wrong"}
```

## Best Practices

1. **Use Type Hints** - Add type hints to lambda functions for better IDE support
2. **Chain with Pipe Operator** - Use `|` for readable sequential composition
3. **Leverage Parallelism** - Use `RunnableParallel` for independent operations
4. **Add Error Handling** - Use `with_retry()` and `with_fallbacks()` for robust chains
5. **Stream When Possible** - Use `.stream()` for better user experience with LLMs
6. **Test Components** - Test individual runnables before composing complex chains

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/expression_language/)
- [LCEL Conceptual Guide](https://python.langchain.com/docs/expression_language/why)
- [Runnable Interface API Reference](https://api.python.langchain.com/en/latest/runnables/langchain_core.runnables.base.Runnable.html)

## License

This guide is provided as-is for educational purposes.