from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

brain = pipeline("text-generation", model="distilgpt2")

memory = []

class Input(BaseModel):
    text: str


@app.post("/chat")
def chat(data: Input):

    memory.append(data.text)

    prompt = "User: " + data.text + "\nAI:"

    out = brain(prompt, max_new_tokens=60, temperature=0.7)

    reply = out[0]["generated_text"].split("AI:")[-1].strip()

    return {"reply": reply}
