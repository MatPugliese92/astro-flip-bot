import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

KEYWORDS = [
    "televue",
    "tele vue",
    "pentax xw",
    "pentax xl",
    "clavé",
    "clave",
    "takahashi",
    "vixen lv",
    "meade series 4000",
    "celestron ultima",
    "oculare astronomico",
    "ortoscopico",
    "skywatcher",
    "celestron",
    "vixen",
    "unitron",
    "zeiss jena"
]

sent = []

for keyword in KEYWORDS:

    url = f"https://www.vinted.com/catalog?search_text={keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text().lower()

    if keyword.lower() in text:

        message = f"🔭 Possibile annuncio trovato su Vinted:\n\n{keyword}\n\n{url}"

        if message not in sent:

            telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

            data = {
                "chat_id": CHAT_ID,
                "text": message
            }

            requests.post(telegram_url, data=data)

            sent.append(message)

            print(f"Inviato alert per: {keyword}")

print("Controllo completato")
