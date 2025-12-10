# LangChain Chaining Guide

## What is Chaining?

Chaining in LangChain refers to the process of connecting multiple components (like prompts, LLMs, parsers, and other tools) together to create complex workflows. Each component's output becomes the input for the next component in the chain.

---

## Why We Need Chaining

### 1. **Break Down Complex Tasks**
- Divide large problems into smaller, manageable steps
- Each step focuses on a specific subtask
- Makes debugging and maintenance easier

### 2. **Reusability**
- Create modular components that can be reused
- Build a library of common chains
- Combine chains in different ways for different use cases

### 3. **Better Control**
- Control the flow of data between components
- Add validation at each step
- Handle errors at specific points in the workflow

### 4. **Improved Accuracy**
- Each step can be optimized independently
- Specialized prompts for specific tasks
- Reduce hallucinations by breaking down reasoning

### 5. **Composability**
- Combine simple chains to create complex workflows
- Mix different LLMs for different tasks
- Integrate external tools and APIs seamlessly

### 6. **Scalability**
- Process multiple requests in parallel
- Optimize performance bottlenecks
- Handle complex enterprise workflows

---

## Types of Chaining

### 1. Sequential Chaining

**Description:**  
Components are executed one after another in a linear sequence. The output of one step becomes the input for the next step.

**Use Cases:**
- Multi-step data processing
- Document summarization → translation → sentiment analysis
- Research → drafting → editing workflows
- Any linear workflow with dependent steps

**Characteristics:**
- ⏱️ Executes in order (Step 1 → Step 2 → Step 3)
- 🔗 Each step depends on the previous step's output
- 📝 Simple and predictable flow
- ⚠️ Slower for independent tasks (no parallelization)

**Example Structure:**
```
Input → Step 1 → Step 2 → Step 3 → Output
```

**Chaining Examples:**

```python
# Basic sequential chain
chain = prompt | model | parser

# Multi-step sequential chain
chain = prompt1 | model | parser | prompt2 | model | parser

# With multiple transformations
chain = prompt | model | output_parser | custom_function | model | parser
```

**Real-World Example:**
```python
# Story → Summary → Sentiment
story_chain = story_prompt | model | parser
summary_chain = summary_prompt | model | parser
sentiment_chain = sentiment_prompt | model | parser

# Complete sequential flow
full_chain = story_chain | summary_chain | sentiment_chain
```

---

### 2. Parallel Chaining

**Description:**  
Multiple chains execute simultaneously on the same input or different inputs. Results are collected and can be combined or processed further.

**Use Cases:**
- Multiple analyses on the same document (sentiment, entities, keywords)
- Comparing outputs from different LLMs
- Processing multiple documents simultaneously
- A/B testing different prompts
- Generating multiple creative variations

**Characteristics:**
- ⚡ Executes simultaneously (faster)
- 🔀 Independent chains don't wait for each other
- 📊 Useful for comparison and aggregation
- 🚀 Better performance for independent tasks

**Example Structure:**
```
           ┌─ Chain A ─┐
Input ────┼─ Chain B ─┼──→ Combine → Output
           └─ Chain C ─┘
```

**Chaining Examples:**

```python
from langchain_core.runnables import RunnableParallel

# Basic parallel execution
parallel_chain = RunnableParallel(
    sentiment=sentiment_prompt | model | parser,
    entities=entities_prompt | model | parser,
    summary=summary_prompt | model | parser
)

# Shorter syntax with dict
parallel_chain = RunnableParallel({
    "sentiment": sentiment_prompt | model | parser,
    "entities": entities_prompt | model | parser,
    "summary": summary_prompt | model | parser
})

# Parallel then combine
chain = RunnableParallel(
    branch1=prompt1 | model | parser,
    branch2=prompt2 | model | parser
) | combine_function

# Batch processing (parallel execution on multiple inputs)
results = (prompt | model | parser).batch([input1, input2, input3])
```

**Real-World Example:**
```python
# Analyze document from multiple perspectives simultaneously
analysis_chain = RunnableParallel(
    sentiment=sentiment_analysis,
    entities=entity_extraction,
    keywords=keyword_extraction,
    category=categorization
) | combine_results
```

---

### 3. Conditional Chaining

**Description:**  
The execution path changes based on conditions or the output of previous steps. Different chains execute based on logic, rules, or LLM decisions.

**Use Cases:**
- Routing queries to specialized models/agents
- Error handling and fallback mechanisms
- Dynamic workflow based on user intent
- Classification-based processing
- Content moderation with different actions

**Characteristics:**
- 🔀 Dynamic execution based on conditions
- 🎯 Routes to appropriate handlers
- 🤔 Can use LLM to make routing decisions
- 🛡️ Implements fallback and error handling

**Example Structure:**
```
Input → Condition Check ─┬─ if A → Chain A → Output
                         ├─ if B → Chain B → Output
                         └─ else → Chain C → Output
```

**Chaining Examples:**

```python
from langchain_core.runnables import RunnableBranch

# Basic conditional routing
conditional_chain = RunnableBranch(
    (condition1, technical_prompt | model | parser),
    (condition2, simple_prompt | model | parser),
    general_prompt | model | parser  # default
)

# With custom condition functions
def is_technical(x):
    return "algorithm" in x["question"].lower()

conditional_chain = RunnableBranch(
    (is_technical, technical_chain),
    (is_simple, simple_chain),
    general_chain  # default
)

# Fallback mechanism
chain = primary_prompt | model | parser
chain_with_fallback = chain.with_fallbacks([
    backup_prompt | model | parser
])

# Retry logic
chain_with_retry = (prompt | model | parser).with_retry(
    stop_after_attempt=3
)
```

**Real-World Example:**
```python
# Route customer support queries
support_router = RunnableBranch(
    (is_urgent, urgent_handler | model | parser),
    (is_refund, refund_handler | model | parser),
    (is_technical, tech_handler | model | parser),
    general_handler | model | parser  # default
)
```

---

## Combining Chain Types

**Complex Workflow Example:**
```python
# Parallel analysis → Conditional routing → Sequential processing
workflow = (
    RunnableParallel(
        sentiment=sentiment_chain,
        topic=topic_chain
    ) 
    | RunnableBranch(
        (is_positive, positive_handler),
        (is_negative, negative_handler),
        neutral_handler
    )
    | final_prompt | model | parser
)
```

**Map-Reduce Pattern:**
```python
# Process in parallel, then combine
map_reduce = (
    RunnableParallel(
        doc1=summarize_chain,
        doc2=summarize_chain,
        doc3=summarize_chain
    )
    | combine_prompt | model | parser
)
```

**Router with Sequential Processing:**
```python
# Route to specialist, then process sequentially
workflow = (
    router 
    | RunnableBranch(
        (condition1, step1 | step2 | step3),
        (condition2, stepA | stepB | stepC),
        default_steps
    )
)
```

---

## Comparison Table

| Feature | Sequential | Parallel | Conditional |
|---------|-----------|----------|-------------|
| **Syntax** | `a \| b \| c` | `RunnableParallel(...)` | `RunnableBranch(...)` |
| **Execution** | One after another | Simultaneous | Based on conditions |
| **Speed** | Slowest | Fastest | Varies |
| **Use Case** | Dependent steps | Independent analyses | Dynamic routing |
| **Complexity** | Simple | Moderate | Complex |
| **Dependencies** | High | None | Conditional |

---

## Common Chaining Patterns

### Pattern 1: Simple Sequential
```python
result = prompt | model | parser
```

### Pattern 2: Multi-Step Sequential
```python
result = step1 | step2 | step3 | step4
```

### Pattern 3: Parallel Execution
```python
result = RunnableParallel(
    output1=chain1,
    output2=chain2
)
```

### Pattern 4: Conditional Routing
```python
result = RunnableBranch(
    (condition, chain_a),
    chain_b  # default
)
```

### Pattern 5: Parallel → Sequential
```python
result = RunnableParallel(
    a=chain_a,
    b=chain_b
) | combine_chain
```

### Pattern 6: Sequential → Conditional
```python
result = step1 | step2 | RunnableBranch(
    (condition, path_a),
    path_b
)
```

### Pattern 7: With Fallback
```python
result = (prompt | model | parser).with_fallbacks([backup_chain])
```

### Pattern 8: With Retry
```python
result = (prompt | model | parser).with_retry(stop_after_attempt=3)
```

### Pattern 9: Batch Processing
```python
results = (prompt | model | parser).batch([input1, input2, input3])
```

### Pattern 10: Complex Nested
```python
result = (
    RunnableParallel(
        analysis1=chain1,
        analysis2=chain2
    )
    | RunnableBranch(
        (condition1, sequential_chain),
        (condition2, another_parallel_chain),
        default_chain
    )
    | final_processor
)
```

---

## Best Practices

### 1. **Choose the Right Chain Type**
- Use **Sequential** (`a | b | c`) for dependent, ordered tasks
- Use **Parallel** (`RunnableParallel(...)`) for independent tasks to improve speed
- Use **Conditional** (`RunnableBranch(...)`) for dynamic, context-aware workflows

### 2. **Keep Chains Simple and Readable**
```python
# Good: Clear and readable
result = prompt | model | parser

# Better: Named components
sentiment_chain = sentiment_prompt | model | parser
result = sentiment_chain | analyzer

# Best: Well-organized complex chains
workflow = (
    preprocessing
    | RunnableParallel(task1=chain1, task2=chain2)
    | postprocessing
)
```

### 3. **Error Handling**
```python
# Always include fallbacks for production
chain = (prompt | model | parser).with_fallbacks([backup_chain])

# Add retry logic
chain = (prompt | model | parser).with_retry(stop_after_attempt=3)
```

### 4. **Performance Optimization**
```python
# Use parallel for independent tasks
parallel = RunnableParallel(
    task1=independent_chain1,
    task2=independent_chain2
)

# Use batch for multiple similar inputs
results = chain.batch([input1, input2, input3])
```

---

## Decision Guide

**When to use Sequential (`|`):**
- Steps depend on each other
- Output of one step is input to next
- Linear workflow
- Example: `translate | summarize | analyze`

**When to use Parallel (`RunnableParallel`):**
- Tasks are independent
- Same input, multiple analyses
- Need to save time
- Example: `RunnableParallel(sentiment=..., entities=..., keywords=...)`

**When to use Conditional (`RunnableBranch`):**
- Different paths for different inputs
- Need routing logic
- Dynamic workflows
- Example: `RunnableBranch((is_urgent, urgent_chain), normal_chain)`

---

## Summary

**The Pipe Operator (`|`):**
- Core chaining mechanism in LangChain
- Connects components sequentially
- Simple and intuitive: `input | step1 | step2 | output`

**Three Main Types:**
1. **Sequential**: `a | b | c` (one after another)
2. **Parallel**: `RunnableParallel(x=a, y=b)` (simultaneous)
3. **Conditional**: `RunnableBranch((condition, a), b)` (dynamic routing)

**Key Takeaway:**  
Mix and match these patterns to build powerful, efficient workflows that handle complex tasks with clarity and performance!