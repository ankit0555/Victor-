
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import uvicorn
import os

app = FastAPI()

# Set your OpenAI key here or through an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-key")

class Query(BaseModel):
    prompt: str
    user_id: str = "default"

memory = {}

@app.post("/query")
async def process_query(query: Query):
    user_prompt = query.prompt
    user_id = query.user_id

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append(user_prompt)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_prompt}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Victor ka system error: {str(e)}"

    return {"reply": reply, "history": memory[user_id][-5:]}

@app.get("/")
async def root():
    return {"Victor": "Online and operational 🚀"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
