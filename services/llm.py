# services/llm.py
import openai
import os

# Try to load environment variables from a .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()  # Loads variables from .env into the environment
except ImportError:
    pass

# Optionally, try to import streamlit and use its secrets if available
try:
    import streamlit as st
except ImportError:
    st = None

# Determine the API key from multiple possible sources
if st is not None and "openai" in st.secrets and "api_key" in st.secrets["openai"]:
    # Use API key from Streamlit secrets when available (e.g., on Streamlit Cloud)
    openai.api_key = st.secrets["openai"]["api_key"]
elif os.getenv("OPENAI_API_KEY"):
    # Use the API key from an environment variable or .env file
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    raise ValueError("No API key set. Please provide one via Streamlit secrets, environment variables, or a .env file.")

def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using an LLM based on the given query and context.
    """
    prompt = (
        f"Using the following context, answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )
    
    response = openai.chat.completions.create(
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        model="gpt-4o",
        max_tokens=150,
        temperature=0.7,
        top_p=1.0
    )
    
    return response.choices[0].message.content
