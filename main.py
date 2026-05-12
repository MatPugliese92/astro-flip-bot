import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = "🚀 Astro Flip Bot online e collegato a Telegram!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=data)

print(response.text)
