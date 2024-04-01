import json
import openai
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest

app = FastAPI()
conversation_history: List[dict] = []

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/chat")
def chat(chat_request: ChatRequest):
    client = openai.OpenAI(api_key="")
    with open('./conversation_history.json', 'r') as f:
        conversation_history: List[dict] = json.load(f)
    conversation_history.append({'role': 'user', 'content': chat_request.message})
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=conversation_history
        )
        conversation_history.append({'role': 'assistant', 'content': response.choices[0].message.content})
        with open('./conversation_history.json', 'w') as f:
            json.dump(conversation_history, f, indent=2)
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        error_message = str(e)
        if "Error code:" in error_message:
            error_code = int(error_message.split("Error code:")[1][:4])
            error_info = error_message.split("Error code:")[1][7:]
            error_msg = "エラーが発生しました、管理者に報告してください。¥nエラーコード:{}¥n詳細:{}".format(error_code, error_info)
            conversation_history.append({'role': 'assistant', 'content': error_message})
            with open('./conversation_history.json', 'w') as f:
                json.dump(conversation_history, f, indent=2)
            raise HTTPException(status_code=400, detail=error_message)