# LangChain Document Loaders

## Overview

Document Loaders are a fundamental component in LangChain that enable you to load data from various sources into a standardized `Document` format. These loaders handle the complexities of reading different file types and data sources, transforming them into a consistent structure that can be processed by other LangChain components.

## What is a Document?

In LangChain, a `Document` is a simple data structure containing:
- `page_content`: The actual text content (string)
- `metadata`: Additional information about the document (dictionary)

```python
from langchain.schema import Document

doc = Document(
    page_content="This is the text content",
    metadata={"source": "example.txt", "page": 1}
)
```

## Why Use Document Loaders?

Document loaders simplify the process of:
- Loading data from multiple source types with a unified interface
- Automatically extracting text and metadata
- Handling various file formats and encodings
- Splitting documents into manageable chunks
- Preparing data for downstream tasks like embeddings and retrieval

## Common Document Loader Types

### File-Based Loaders

**TextLoader**
- Loads plain text files
- Simple and straightforward for `.txt` files

```python
from langchain.document_loaders import TextLoader

loader = TextLoader("path/to/file.txt")
documents = loader.load()
```

**CSVLoader**
- Loads data from CSV files
- Each row becomes a document

```python
from langchain.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path="data.csv")
documents = loader.load()
```

**JSONLoader**
- Loads JSON files with customizable content extraction
- Uses jq schema for complex JSON structures

```python
from langchain.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="data.json",
    jq_schema=".messages[].content",
    text_content=False
)
documents = loader.load()
```

**PDFLoader**
- Multiple implementations available (PyPDF, PyMuPDF, PDFPlumber)
- Extracts text from PDF documents

```python
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
pages = loader.load_and_split()
```

**UnstructuredFileLoader**
- Handles multiple file types (PDF, DOCX, HTML, etc.)
- Uses the Unstructured library for advanced parsing

```python
from langchain.document_loaders import UnstructuredFileLoader

loader = UnstructuredFileLoader("document.docx")
documents = loader.load()
```

### Directory Loaders

**DirectoryLoader**
- Loads all files from a directory
- Supports glob patterns and file filtering

```python
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    "path/to/directory",
    glob="**/*.txt",
    show_progress=True
)
documents = loader.load()
```

### Web-Based Loaders

**WebBaseLoader**
- Loads content from web URLs
- Uses BeautifulSoup for HTML parsing

```python
from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
documents = loader.load()
```

**SitemapLoader**
- Crawls and loads content from website sitemaps

```python
from langchain.document_loaders.sitemap import SitemapLoader

loader = SitemapLoader("https://example.com/sitemap.xml")
documents = loader.load()
```

### Database Loaders

**SQLDatabaseLoader**
- Loads data from SQL databases
- Executes queries and converts results to documents

```python
from langchain.document_loaders import SQLDatabaseLoader

loader = SQLDatabaseLoader(
    query="SELECT * FROM articles",
    db=database_connection
)
documents = loader.load()
```

### Cloud Storage Loaders

**S3FileLoader / S3DirectoryLoader**
- Loads files from Amazon S3 buckets

```python
from langchain.document_loaders import S3FileLoader

loader = S3FileLoader("bucket-name", "file-key.txt")
documents = loader.load()
```

**GCSFileLoader / GCSDirectoryLoader**
- Loads files from Google Cloud Storage

```python
from langchain.document_loaders import GCSFileLoader

loader = GCSFileLoader(
    project_name="project-id",
    bucket="bucket-name",
    blob="file.txt"
)
documents = loader.load()
```

### Specialized Loaders

**GitLoader**
- Loads files from Git repositories

**NotionDBLoader**
- Loads pages from Notion databases

**SlackDirectoryLoader**
- Loads messages from Slack channels

**ConfluenceLoader**
- Loads pages from Confluence

**GoogleDriveLoader**
- Loads documents from Google Drive

## Basic Usage Pattern

All document loaders follow a similar interface:

```python
# 1. Import the loader
from langchain.document_loaders import SomeLoader

# 2. Initialize with configuration
loader = SomeLoader(
    source="path/to/source",
    # Additional parameters
)

# 3. Load documents
documents = loader.load()

# 4. Access document content and metadata
for doc in documents:
    print(doc.page_content)
    print(doc.metadata)
```

## Advanced Features

### Lazy Loading vs Eager Loading

Document loaders in LangChain support two loading strategies:

#### Eager Loading with `load()`

The `load()` method implements **eager loading** - it loads all documents into memory at once and returns them as a list. This is the default behavior.

**Characteristics:**
- Loads all documents immediately into memory
- Returns a `List[Document]`
- Simple to use and understand
- Best for small to medium-sized datasets
- Allows immediate access to all documents

```python
loader = TextLoader("document.txt")
documents = loader.load()  # All documents loaded at once
print(f"Loaded {len(documents)} documents")

# Can immediately iterate through all documents
for doc in documents:
    print(doc.page_content)
```

**When to use `load()`:**
- Working with small datasets that fit comfortably in memory
- Need to know the total count of documents upfront
- Require random access to documents
- Performing operations that need the entire dataset (sorting, filtering, etc.)

#### Lazy Loading with `lazy_load()`

The `lazy_load()` method implements **lazy loading** - it loads documents one at a time as they're requested, using a generator pattern.

**Characteristics:**
- Loads documents on-demand, one at a time
- Returns an `Iterator[Document]`
- Memory-efficient for large datasets
- Streaming approach - processing starts immediately
- Lower initial latency

```python
loader = TextLoader("large_file.txt")

# Documents are loaded one at a time as you iterate
for document in loader.lazy_load():
    # Process each document individually
    # Previous documents can be garbage collected
    process(document)
```

**When to use `lazy_load()`:**
- Working with large files or datasets that might not fit in memory
- Processing documents in a streaming fashion
- Want to start processing immediately without waiting for all data to load
- Need to minimize memory footprint
- Processing can be done independently on each document

#### Comparison Table

| Feature | `load()` (Eager) | `lazy_load()` (Lazy) |
|---------|------------------|----------------------|
| **Memory Usage** | High - all documents in memory | Low - one document at a time |
| **Initial Wait Time** | Longer - loads everything first | Shorter - starts immediately |
| **Return Type** | `List[Document]` | `Iterator[Document]` |
| **Random Access** | Yes - can access any document | No - sequential only |
| **Best For** | Small to medium datasets | Large datasets, streaming |
| **Processing Start** | After all documents loaded | Immediate |
| **Total Document Count** | Known immediately | Unknown until iteration completes |

#### Practical Example Comparison

```python
from langchain.document_loaders import TextLoader

# Eager Loading - Good for small files
loader = TextLoader("small_file.txt")
all_docs = loader.load()
print(f"Total documents: {len(all_docs)}")  # Know count immediately
first_doc = all_docs[0]  # Random access
last_doc = all_docs[-1]

# Lazy Loading - Better for large files
loader = TextLoader("large_file.txt")
doc_count = 0
for doc in loader.lazy_load():
    doc_count += 1
    # Process document immediately
    if some_condition(doc):
        break  # Can stop early, saving time and memory
print(f"Processed {doc_count} documents")
```

#### Best Practice: Hybrid Approach

For optimal performance, use a combination:

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Use lazy_load for initial loading
loader = DirectoryLoader("./large_dataset", glob="**/*.txt")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

# Process in batches
batch = []
batch_size = 100

for doc in loader.lazy_load():
    batch.append(doc)
    
    if len(batch) >= batch_size:
        # Process batch
        split_docs = text_splitter.split_documents(batch)
        # Store or process split_docs
        batch = []  # Clear for next batch

# Process remaining documents
if batch:
    split_docs = text_splitter.split_documents(batch)
```

### Document Splitting

Combine loaders with text splitters for better chunking:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = TextLoader("document.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
split_docs = text_splitter.split_documents(documents)
```

## Installation

Most loaders require additional dependencies:

```bash
# Core loaders
pip install langchain

# PDF support
pip install pypdf

# Unstructured file support
pip install unstructured

# Web scraping
pip install beautifulsoup4

# Cloud storage
pip install boto3  # AWS S3
pip install google-cloud-storage  # GCS
```

## Best Practices

1. **Choose the right loader**: Select a loader optimized for your data source
2. **Handle errors gracefully**: Implement try-catch blocks for file operations
3. **Process metadata**: Preserve important metadata for better document tracking
4. **Use lazy loading**: For large datasets to manage memory efficiently
5. **Split appropriately**: Combine with text splitters for optimal chunk sizes
6. **Test with samples**: Verify loader behavior with sample data first

## Next Steps

For more advanced use cases, we may need to create a custom document loader. See the [Custom Document Loader Guide](./CUSTOM_DOCUMENT_LOADER.md) for detailed instructions on implementing your own loader.

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
- [Document Loaders API Reference](https://api.python.langchain.com/en/latest/document_loaders.html)
- [Community Integrations](https://python.langchain.com/docs/integrations/document_loaders/)