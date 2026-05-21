import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

PDF_DIR = "../data"
CHROMA_DIR = "../chroma_db"

def ingest():
    docs = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_DIR, file)
            loader = PyMuPDFLoader(path)
            docs.extend(loader.load())
            print(f"Loaded: {file}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Total chunks: {len(chunks)}")

    embeddings = FastEmbedEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print("Ingestion complete. Vectorstore saved.")

if __name__ == "__main__":
    ingest()