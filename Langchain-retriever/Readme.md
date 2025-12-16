# Information Retrieval Systems

## What is a Retriever?

A retriever is a component in information retrieval systems that efficiently searches and fetches relevant documents or information from a data source based on a user's query. Retrievers act as the bridge between large data repositories and end-users, enabling quick access to pertinent information without requiring manual searching through entire datasets.

In modern AI applications, particularly in Retrieval-Augmented Generation (RAG) systems, retrievers play a crucial role by finding contextually relevant documents that can augment language model responses with accurate, up-to-date information.

---

## Types of Retrievers

### 1. Wikipedia Retriever

**What it is:**
A specialized retriever that searches and fetches content directly from Wikipedia articles. It leverages Wikipedia's API to access its vast knowledge base of structured, encyclopedic information.

**Ideal use cases:**
- General knowledge questions requiring factual, encyclopedic information
- Educational applications needing authoritative reference material
- Systems requiring well-structured, community-validated content
- Quick fact-checking and background research
- Applications where citation to a reliable source is important

---

### 2. Vector Store Retriever

**What it is:**
A retriever that uses vector embeddings to represent documents and queries in a high-dimensional space. It searches by measuring semantic similarity between the query vector and document vectors stored in a vector database (like Pinecone, Chroma, or FAISS).

**Ideal use cases:**
- Semantic search where meaning matters more than exact keyword matches
- Large document collections requiring fast similarity search
- Applications needing to find conceptually related content
- Multilingual search scenarios
- Custom knowledge bases with domain-specific content
- When you need to capture nuanced relationships between queries and documents

---

### 3. MMR (Maximal Marginal Relevance) as Search Type

**What it is:**
A search algorithm that balances relevance and diversity in search results. Instead of returning only the most similar documents, MMR selects documents that are both relevant to the query and different from each other, reducing redundancy.

**Ideal use cases:**
- When you want diverse perspectives on a topic
- Avoiding redundant or repetitive information in results
- Exploratory research where variety is valuable
- Summarization tasks requiring comprehensive coverage
- Situations where the top results might be too similar
- User-facing applications where result diversity improves experience

---

### 4. Multi-Query Retriever

**What it is:**
A retriever that generates multiple variations of the original user query and retrieves documents for each variation, then combines and deduplicates the results. This approach helps overcome the limitation of a single query formulation and captures different aspects of the user's information need.

**Ideal use cases:**
- Complex or ambiguous queries that could be interpreted multiple ways
- Improving recall by capturing documents that might be missed with a single query
- Questions that have multiple relevant facets or angles
- When query reformulation could significantly improve results
- Overcoming vocabulary mismatch between query and documents
- Research scenarios requiring comprehensive coverage

---

### 5. Contextual Compression Retriever

**What it is:**
A retriever that first fetches relevant documents and then compresses or filters them to extract only the most relevant portions. It uses a compression algorithm or model to remove irrelevant content, reducing noise and focusing on the most pertinent information.

**Ideal use cases:**
- Long documents where only small sections are relevant
- Reducing token usage in language model applications
- Improving precision when documents contain mixed content
- Speeding up downstream processing by removing unnecessary text
- Applications with context window limitations
- When you need to extract specific information from verbose documents

---

## Other Retriever Types

- **BM25 Retriever** - Traditional keyword-based ranking algorithm
- **TF-IDF Retriever** - Term frequency-inverse document frequency based retrieval
- **Ensemble Retriever** - Combines multiple retrievers
- **Self-Query Retriever** - Extracts filters from natural language queries
- **Time-Weighted Retriever** - Prioritizes recent documents
- **Parent Document Retriever** - Retrieves larger context around matched chunks
- **Long Context Reorder** - Reorders documents for optimal context placement
- **Cohere Rerank Retriever** - Uses Cohere's reranking API
- **kNN Retriever** - k-Nearest Neighbors based retrieval
- **SVM Retriever** - Support Vector Machine based retrieval
- **Hybrid Retriever** - Combines sparse and dense retrieval methods
- **Web Search Retriever** - Retrieves from search engines (Google, Bing, DuckDuckGo)
- **Arxiv Retriever** - Searches academic papers on Arxiv
- **PubMed Retriever** - Searches biomedical literature

---

## Other Search Types

- **Similarity Search** - Basic vector similarity (cosine, euclidean, dot product)
- **Similarity Score Threshold** - Filters by minimum similarity score
- **Top-K Search** - Returns fixed number of top results
- **Threshold-based Search** - Returns all results above a threshold
- **Hybrid Search** - Combines keyword and semantic search
- **Filtered Search** - Applies metadata filters before retrieval
- **ANN (Approximate Nearest Neighbor)** - Fast approximate similarity search
- **Multi-vector Search** - Uses multiple embedding vectors per document
- **Sparse-Dense Hybrid** - Combines BM25/TF-IDF with vector search

---

## Choosing the Right Retriever

The choice of retriever depends on several factors:

- **Data source type** (Wikipedia, custom documents, web, databases)
- **Query complexity** (simple keywords vs. complex questions)
- **Performance requirements** (speed, accuracy, recall)
- **Result requirements** (precision, diversity, comprehensiveness)
- **Resource constraints** (computational power, storage, API costs)
- **Domain specificity** (general knowledge vs. specialized content)

Many modern systems use multiple retrievers in combination to leverage the strengths of each approach.


# Resources:
- [LangChain Retriever Documentation](https://docs.langchain.com/oss/python/integrations/retrievers)

### Note
- If someone talk about Advance RAG he/she is directly talking about this retriever only.