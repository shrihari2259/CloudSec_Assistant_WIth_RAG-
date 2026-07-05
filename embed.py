import os
from dotenv import load_dotenv
load_dotenv()

os.environ["USER_AGENT"] = "cloudsec-assistant/1.0"

from ingest import load_docs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

documents = load_docs()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_documents(documents)
print(f"Prepared {len(chunks)} chunks for embedding")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if index_name not in [i.name for i in pc.list_indexes()]:
    print(f"Creating Pinecone index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
else:
    print(f"Index {index_name} already exists")

print("Downloading embedding model (first run only, ~90MB)...")
print("Uploading to Pinecone... this may take a few minutes")
vectorstore = PineconeVectorStore.from_documents(
    chunks, embeddings, index_name=index_name
)
print("Done! All chunks embedded and stored in Pinecone.")
