import os
from dotenv import load_dotenv

load_dotenv()

USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"

if USE_OLLAMA:
    try:
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(model=os.getenv("OLLAMA_MODEL", "phi"))
        reviewer_llm = OllamaLLM(model=os.getenv("OLLAMA_MODEL", "phi"))
        print("🔗 Using Ollama model:", os.getenv("OLLAMA_MODEL", "phi"))
    except ImportError:
        from langchain_community.llms import Ollama
        llm = Ollama(model=os.getenv("OLLAMA_MODEL", "phi"), temperature=0)
        reviewer_llm = Ollama(model=os.getenv("OLLAMA_MODEL", "phi"), temperature=0)
        print("⚠️ Using deprecated Ollama import.")
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    reviewer_llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    print("🔗 Using OpenAI model:", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
