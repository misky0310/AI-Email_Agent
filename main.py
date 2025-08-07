import gradio as gr
from email_handling.email_loader import fetch_emails
from vector_store.chroma_store import build_vectorstore
from rag.rag_query import get_response

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GMAIL_USER_STUDENT")
app_password = os.getenv("GMAIL_APP_PASSWORD_STUDENT")


# Step 1: Load and Vectorize Emails
def load_and_vectorize():
    try:
        emails = fetch_emails("imap.gmail.com", username, app_password)
        build_vectorstore(emails)
        return "Successfully loaded and vectorized emails."
    except Exception as e:
        return f"Error: {str(e)}"


# Step 2: Ask Query
def query_email_knowledge(query):
    try:
        response = get_response(query)
        return response
    except Exception as e:
        return f"Error during response generation: {str(e)}"


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📬 Email AI Agent (RAG Pipeline)")

    with gr.Row():
        load_button = gr.Button("📥 Load & Vectorize Emails")
        status_box = gr.Textbox(label="Status", interactive=False)

    load_button.click(fn=load_and_vectorize, outputs=status_box)

    gr.Markdown("---")
    gr.Markdown("### 🤖 Ask Questions about Your Emails")

    query_input = gr.Textbox(label="Your Question", placeholder="e.g., What deadlines should I be aware of?")
    response_output = gr.Textbox(label="AI Response")

    query_input.submit(fn=query_email_knowledge, inputs=query_input, outputs=response_output)

if __name__ == "__main__":
    demo.launch()
