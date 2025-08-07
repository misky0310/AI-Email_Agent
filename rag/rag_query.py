from vector_store.chroma_store import semantic_search
from langchain_community.llms import Ollama

llm=Ollama(model="llama3.2")

def get_response(query):

    # Perform semantic search in vector store
    relevant_docs = semantic_search(query)

    # Handle empty retrieval case
    if not relevant_docs:
        return "No relevant emails found for your query."

    # Extract unique document contents using their page_content
    seen = set()
    unique_contents = []
    for doc, _ in relevant_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_contents.append(doc.page_content)

    # Add the relevant docs as context to the LLM input
    print("Adding relevant docs to the LLM input...")
    context = "\n\n".join(unique_contents)

    #frame the prompt
    prompt=f'''
                You are an expert AI assistant helping the user understand their emails.
                Use the following email content to answer the question.
                
                Email Context : {context}

                User Question: {query}
            '''

    # Call the LLM to generate an answer
    try:
        print("Invoking the LLM...")
        response=llm.invoke(prompt)
        print("Successfully generated the response.)")
        return response
    except Exception as e:
        return f'An error occurred while generating the response: {str(e)}'