from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path='books',
    glob='*.pdf',   # The glob helps to filter the files in the directory which we want to load
    loader_cls=PyPDFLoader
)
# lazy_load doesn't load all the files at once it loads one by one, whereas load loads all the files at once
docs = loader.lazy_load()

for document in docs:
    print(document.metadata)