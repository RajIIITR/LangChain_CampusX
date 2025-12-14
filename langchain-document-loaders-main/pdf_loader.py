from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('dl-curriculum.pdf')

docs = loader.load()

print(len(docs))
# PyPDFLoader returns a list of documents each having a page content and metadata
print(docs[0].page_content)
print(docs[1].metadata)