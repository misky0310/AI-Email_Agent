# rag/rag_query.py
from vector_store.chroma_store import get_vectorstore
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama3.2")

# Define a custom prompt
prompt_template = """
You are an expert AI assistant helping the user understand their emails.
Use the provided email content to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Create the QA chain
def get_response(query: str):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    try:
        print("Querying vectorstore with RAG...")
        result = qa_chain.invoke({"query": query})
        return result["result"]
    except Exception as e:
        return f"Error while generating response: {e}"
