import os
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vectorstore = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX"),
    embedding=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def is_in_domain(question: str) -> bool:
    check = llm.invoke(f"""Answer only YES or NO.
Is this question about cloud computing, AWS/Azure/GCP, DevOps, or cybersecurity?
Question: {question}""")
    return "YES" in check.content.upper()

def ask(question: str):
    if not is_in_domain(question):
        return {
            "answer": "I only answer cloud computing and cybersecurity questions.",
            "sources": []
        }

    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    sources = list(set(d.metadata.get("source", "unknown") for d in docs))

    prompt = f"""Answer the question using ONLY the context below. If the context doesn't contain the answer, say so.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke(prompt)
    return {"answer": response.content, "sources": sources}

if __name__ == "__main__":
    print(ask("cloud security best practices for AWS?   "))
    print("---")
    print(ask("What's a good pizza recipe?"))
