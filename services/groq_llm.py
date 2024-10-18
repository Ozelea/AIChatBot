from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
GROQ_API_KEY=os.getenv('GROQ_API_KEY')

# Initialize the LLM

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.7,
    max_tokens=150,
    api_key=GROQ_API_KEY
)
