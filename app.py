import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
TOKEN = os.getenv("TOKEN")

def chat_stream(user_text):
    # 如果你是用的是硅基流动，可以直接使用下面的URL
    # url = "https://api.siliconflow.cn/v1/chat/completions"
    url = "https://api.gptsapi.net/v1/chat/completions"
    payload = {
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": user_text}],
        "stream": True
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    with requests.post(url, headers=headers, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8").strip()
            if decoded == "data: [DONE]":
                break
            if decoded.startswith("data: "):
                try:
                    data_json = json.loads(decoded[len("data: "):])
                    choices = data_json.get("choices", [])
                    for choice in choices:
                        delta = choice.get("delta", {})
                        text = delta.get("content")
                        if text:
                            print(text, end="", flush=True)
                except json.JSONDecodeError:
                    continue

if __name__ == "__main__":
    print("SiliconFlow ChatBot")
    while True:
        user_input = input("\n你: ")
        print("AI: ", end="", flush=True)
        chat_stream(user_input)
        print()
