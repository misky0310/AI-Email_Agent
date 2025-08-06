import uuid
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from embedder import embedding_model

PERSIST_DIR = "./chroma_store"
COLLECTION_NAME = "emails"

#inside each function , make it global so as to use it across different functions
chroma_db = None

#Creates or reuses a persistent vectorstore.
def build_vectorstore(email_dicts: list):

    global chroma_db

    docs = []
    for email in email_dicts:
        doc = Document(
            page_content=email["Body"],
            metadata={
                "subject": email.get("Subject", ""),
                "from": email.get("From", ""),
                "id": str(uuid.uuid4())
            }
        )
        docs.append(doc)

    if not chroma_db:
        chroma_db = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=PERSIST_DIR
        )

    chroma_db.add_documents(docs)
    chroma_db.persist()

    return chroma_db

def semantic_search(query: str, k: int = 5):

    global chroma_db

    if not chroma_db:
        chroma_db = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=PERSIST_DIR
        )

    return chroma_db.similarity_search(query, k=k)
