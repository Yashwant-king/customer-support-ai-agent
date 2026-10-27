from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq


#qwen/qwen3.8-27b
#openai/gpt-oss-20b


try:
    llm=ChatGroq(model="qwen/qwen3.8-27b")
    print("LLM initialized successfully.")
except Exception as e:
    print(f"Error initializing LLM: {e}")
    print("Second LLM has initialized successfully.")
    llm=ChatGroq(model="openai/gpt-oss-20b")









