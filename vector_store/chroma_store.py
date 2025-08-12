# vector_store/chroma_store.py
import uuid
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vector_store.embedder import embedding_model

PERSIST_DIR = "./chroma_store"
COLLECTION_NAME = "emails"

def build_vectorstore(email_dicts: list):
    print("Creating or reusing vectorstore...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = []
    for email in email_dicts:
        chunks = splitter.split_text(email["Body"])
        for chunk in chunks:
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "subject": email.get("Subject", ""),
                        "from": email.get("From", ""),
                        "id": str(uuid.uuid4())
                    }
                )
            )

    db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=PERSIST_DIR
    )

    db.add_documents(docs)
    db.persist()
    print(f"Vectorstore updated with {len(docs)} chunks.")
    return db

def get_vectorstore():
    """Load existing Chroma vectorstore"""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=PERSIST_DIR
    )
