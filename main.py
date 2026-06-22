from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

memory = []

class Input(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "TetoAI is running"}

@app.post("/chat")
def chat(data: Input):
    memory.append(data.text)

    user_text = data.text.strip()

    if "hello" in user_text.lower():
        reply = "Hello! It's nice to talk with you."
    elif "how are you" in user_text.lower():
        reply = "I'm doing well and ready to chat."
    else:
        reply = f"You said: {user_text}"

    return {"reply": reply}
