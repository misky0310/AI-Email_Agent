#File to initialise the embedding model and can be imported in other files
from langchain_ollama import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model='nomic-embed-text')