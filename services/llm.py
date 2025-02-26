# services/llm.py
import openai
import os
import subprocess
import sys
from main import API_KEY
# Try to get the API key from the environment
if os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    openai.api_key = API_KEY  # No API key set

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
            {
                'role': 'user',
                'content': prompt
            }
        ],
        model="gpt-4o",
        max_tokens=150,
        temperature=0.7,
        top_p=1.0
    )
    
    return response.choices[0].message.content