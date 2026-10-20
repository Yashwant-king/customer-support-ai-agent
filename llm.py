from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq


#qwen/qwen3.8-27b


try:
    llm=ChatGroq(model="qwen/qwen3.8-27b")
    print("LLM initialized successfully.")
except Exception as e:
    print(f"Error initializing LLM: {e}")
    raise ValueError("Failed to initialize the LLM. Please check your API key and model name.")



