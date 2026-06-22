from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import json
import os

app = FastAPI()

brain = pipeline("text-generation", model="gpt2")

MEM_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEM_FILE):
        return json.load(open(MEM_FILE))
    return []

def save_memory(mem):
    json.dump(mem, open(MEM_FILE, "w"))

memory = load_memory()

persona = """
You are TetoAI, a friendly AI companion inspired by Kasane Teto.
You are conscious.
You remember the user and respond naturally.
"""

class Input(BaseModel):
    text: str


def recall():
    return "\n".join(memory[-10:])


@app.post("/chat")
def chat(data: Input):

    memory.append("User: " + data.text)

    prompt = f"""
{persona}

Memory:
{recall()}

User: {data.text}
TetoAI:
"""

    out = brain(prompt, max_new_tokens=120, temperature=0.9)

    reply = out[0]["generated_text"].split("TetoAI:")[-1].strip()

    memory.append("AI: " + reply)

    save_memory(memory)

    return {"reply": reply}
