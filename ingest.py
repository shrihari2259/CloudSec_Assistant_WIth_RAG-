import os
os.environ["USER_AGENT"] = "cloudsec-assistant/1.0"

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_docs():
    docs = []
    pdf_files = ["data/well_architected.pdf", "data/nist_csf.pdf"]
    for f in pdf_files:
        docs.extend(PyPDFLoader(f).load())

    web_urls = ["https://owasp.org/www-project-top-ten/"]
    for url in web_urls:
        docs.extend(WebBaseLoader(url).load())

    return docs

if __name__ == "__main__":
    documents = load_docs()
    print(f"Loaded {len(documents)} raw documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
