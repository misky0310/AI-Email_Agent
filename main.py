import gradio as gr
import os
from dotenv import load_dotenv

from email_handling.email_loader import fetch_emails
from vector_store.chroma_store import build_vectorstore
from rag.rag_query import get_response  # <- Now uses RetrievalQA internally

# Load environment variables
load_dotenv()
username = os.getenv("GMAIL_USER_STUDENT")
app_password = os.getenv("GMAIL_APP_PASSWORD_STUDENT")

# Step 1: Load & Vectorize Emails
def load_and_vectorize():
    try:
        emails = fetch_emails("imap.gmail.com", username, app_password)
        if not emails:
            return "No emails retrieved. Please check your email credentials or filters."

        build_vectorstore(emails)  # Chunks & embeds inside Chroma
        return f"✅ Successfully loaded {len(emails)} emails into the vectorstore."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Step 2: Query RAG
def query_email_knowledge(query):
    try:
        if not query.strip():
            return "Please enter a question."
        response = get_response(query)  # RetrievalQA chain
        return response
    except Exception as e:
        return f"❌ Error during response generation: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📬 Email AI Agent — Retrieval-Augmented Generation")

    with gr.Row():
        load_button = gr.Button("📥 Load & Vectorize Emails")
        status_box = gr.Textbox(label="Status", interactive=False)

    load_button.click(fn=load_and_vectorize, outputs=status_box)

    gr.Markdown("---")
    gr.Markdown("### 🤖 Ask Questions About Your Emails")

    query_input = gr.Textbox(
        label="Your Question",
        placeholder="e.g., What deadlines should I be aware of?",
    )
    response_output = gr.Textbox(label="AI Response", lines=8)

    query_input.submit(fn=query_email_knowledge, inputs=query_input, outputs=response_output)

if __name__ == "__main__":
    demo.launch()
