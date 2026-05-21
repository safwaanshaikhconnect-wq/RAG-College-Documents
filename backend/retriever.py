import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "../chroma_db"

def load_retriever():
    embeddings = FastEmbedEmbeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def format_docs(docs):
    return "\n\n".join(
        f"[Page {doc.metadata.get('page', '?')}]: {doc.page_content}"
        for doc in docs
    )

def build_chain():
    retriever = load_retriever()

    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question using only the context below.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}
""")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if __name__ == "__main__":
    chain = build_chain()
    while True:
        query = input("\nAsk a question (or 'quit'): ")
        if query.lower() == "quit":
            break
        answer = chain.invoke(query)
        print(f"\nAnswer: {answer}")