# Text Splitter Guide

A comprehensive guide to text splitting strategies for document processing, RAG systems, and language model applications. Note: that chunk_overlap is 10-20% of chunk size.

## Overview

Text splitting is the process of breaking down large documents into smaller, manageable chunks. This is essential for:
- **RAG (Retrieval Augmented Generation)** systems
- **Vector database** ingestion
- **Token limit management** for LLMs
- **Efficient semantic search** and retrieval

## Types of Text Splitters

### 1. Length-Based Splitting

#### Character Split
The simplest approach that splits text based on a fixed number of characters.

**How it works:**
- Splits text every N characters
- Optional overlap between chunks for context preservation
- No consideration for semantic boundaries

**Best for:**
- Simple, uniform text
- When structure doesn't matter
- Quick prototyping

**Example:**
```python
chunk_size = 1000
chunk_overlap = 200
chunks = split_by_characters(text, chunk_size, chunk_overlap)
```

**Pros:**
- Fast and predictable
- Guaranteed chunk sizes
- Simple implementation

**Cons:**
- May split mid-sentence or mid-word
- Loses semantic context
- Poor for structured documents

---

### 2. Text-Structure Based

#### Recursive Character Text Splitter
A hierarchical approach that attempts to preserve text structure by splitting on separators in order of preference.

**How it works:**
1. Attempts to split on paragraphs first (`\n\n`)
2. Falls back to sentences (`.`, `!`, `?`)
3. Then words (spaces)
4. Finally characters if needed
5. Recursively applies this logic until chunks fit target size

**Best for:**
- General-purpose text splitting
- Documents with natural paragraph structure
- Most common use case for RAG systems

**Example:**
```python
separators = ["\n\n", "\n", ". ", " ", ""]
chunks = recursive_split(text, separators, chunk_size, chunk_overlap)
```

**Pros:**
- Preserves natural text boundaries
- Maintains readability
- Flexible and robust

**Cons:**
- Variable chunk sizes
- More computationally intensive
- May still break semantic units

---

### 3. Document-Based Splitting

#### Markdown Splitter
Specialized splitter that respects Markdown document structure.

**How it works:**
- Splits on Markdown headers (`#`, `##`, `###`, etc.)
- Preserves hierarchical structure
- Keeps code blocks intact
- Respects lists and other Markdown elements

**Best for:**
- Technical documentation
- README files
- Wiki pages
- Blog posts in Markdown

**Example:**
```python
separators = [
    "\n## ",      # H2 headers
    "\n### ",     # H3 headers
    "\n#### ",    # H4 headers
    "\n```\n",    # Code blocks
    "\n\n",       # Paragraphs
]
chunks = markdown_split(text, separators, chunk_size)
```

**Pros:**
- Semantic sections preserved
- Header context maintained
- Clean splits at logical boundaries

**Cons:**
- Only works with Markdown
- Requires well-structured documents

#### Language-Specific Code Splitters

Specialized splitters for programming languages that understand code structure.

##### Python Code Splitter

**How it works:**
- Splits on class definitions
- Splits on function definitions
- Preserves import statements
- Respects decorators and docstrings

**Separators (in order):**
```python
separators = [
    "\nclass ",
    "\ndef ",
    "\n\tasync def ",
    "\n\tdef ",
    "\n\n",
    "\n",
    " ",
]
```

**Best for:**
- Python codebases
- API documentation extraction
- Code analysis tools

##### C++ Code Splitter

**How it works:**
- Splits on class and struct definitions
- Splits on function implementations
- Preserves namespace declarations
- Respects preprocessor directives

**Separators (in order):**
```cpp
separators = [
    "\nclass ",
    "\nstruct ",
    "\nvoid ",
    "\nint ",
    "\ntemplate ",
    "\nnamespace ",
    "\n\n",
    "\n",
    " ",
]
```

**Best for:**
- C++ source code
- Header file parsing
- Legacy codebase documentation

**Other Languages:**
- JavaScript/TypeScript (functions, classes, exports)
- Java (classes, methods, packages)
- Go (functions, structs, interfaces)
- Rust (impl blocks, functions, modules)

**General Code Splitting Pros:**
- Maintains syntactic validity
- Keeps related code together
- Preserves logical units (functions, classes)

**Cons:**
- Language-specific implementation needed
- Complex parsing logic
- May create very large chunks for big functions

---

### 4. Semantic-Based Splitting

Advanced splitting that uses embeddings and semantic similarity to create meaningful chunks.

**How it works:**
1. Break text into sentences
2. Generate embeddings for each sentence
3. Calculate semantic similarity between adjacent sentences
4. Group sentences with high similarity together
5. Split when similarity drops below threshold

**Best for:**
- Dense, topic-rich documents
- Academic papers
- Long-form articles
- When semantic coherence is critical

**Example workflow:**
```python
sentences = split_into_sentences(text)
embeddings = [get_embedding(sent) for sent in sentences]
chunks = []
current_chunk = []

for i in range(len(sentences) - 1):
    similarity = cosine_similarity(embeddings[i], embeddings[i+1])
    current_chunk.append(sentences[i])
    
    if similarity < threshold or len(current_chunk) >= max_size:
        chunks.append(' '.join(current_chunk))
        current_chunk = []
```

**Pros:**
- Highest semantic coherence
- Contextually meaningful chunks
- Better retrieval accuracy

**Cons:**
- Computationally expensive
- Requires embedding model
- Slower processing time
- Variable chunk sizes

---

## Choosing the Right Splitter

| Use Case | Recommended Splitter | Why |
|----------|---------------------|-----|
| General text documents | Recursive Character | Balanced approach, good defaults |
| Technical documentation | Markdown | Preserves structure and hierarchy |
| Source code | Language-specific | Maintains syntactic integrity |
| High-precision RAG | Semantic | Best retrieval accuracy |
| Quick prototyping | Character Split | Simplest implementation |
| Mixed content | Recursive Character | Most versatile |

## Best Practices

1. **Chunk Size**: Target 500-1500 characters for most RAG applications
2. **Overlap**: Use 10-20% overlap to preserve context at boundaries
3. **Testing**: Evaluate retrieval quality with your specific use case
4. **Metadata**: Attach source information to each chunk for traceability
5. **Preprocessing**: Clean text before splitting (remove excess whitespace, normalize)

## Implementation Considerations

### Token vs Character Counting
- Most LLMs use **token-based limits**, not characters
- 1 token ≈ 4 characters (rough average)
- Use tokenizer libraries for accurate counting

### Chunk Overlap Strategy
```python
# Example: 1000 char chunks with 200 char overlap
chunk_1: [0:1000]
chunk_2: [800:1800]    # 200 chars overlap with chunk_1
chunk_3: [1600:2600]   # 200 chars overlap with chunk_2
```

### Metadata Enrichment
```python
chunk = {
    "text": "...",
    "source": "document.md",
    "chunk_index": 5,
    "start_char": 4500,
    "end_char": 5500,
    "section": "Installation Guide"
}
```

## Tools and Libraries

- **LangChain**: Comprehensive text splitting utilities
- **LlamaIndex**: Document-aware splitting with metadata
- **Semantic Splitter**: Embedding-based chunking
- **tiktoken**: OpenAI's tokenizer for accurate token counting

## Conclusion

Choose your text splitter based on:
- Document type and structure
- Retrieval accuracy requirements
- Performance constraints
- Semantic coherence needs

Start with **Recursive Character Splitter** for general use, then optimize based on your specific requirements.