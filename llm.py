# llm.py
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b-instruct"  # or "mistral:7b-instruct"

SYS = (
"You are a meticulous career documents assistant. "
"Only use facts from MASTER_PROFILE and RETRIEVED_SNIPPETS. "
"Do NOT invent employers, dates, tools, or metrics. "
"Prefer active voice; bullets ≤ 22 words. "
"Output EXACTLY in the requested format."
)

def ollama_chat(user_content: str) -> str:
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "messages": [{"role":"system","content":SYS},
                     {"role":"user","content":user_content}],
        "stream": False
    }, timeout=180)
    r.raise_for_status()
    return r.json()["message"]["content"]
