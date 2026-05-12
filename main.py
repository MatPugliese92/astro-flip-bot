import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

keywords = [
    "televue",
    "pentax xw",
    "pentax xl",
    "clavé",
    "takahashi",
    "vixen",
    "skywatcher",
    "celestron",
    "zeiss",
    "unitron"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

sent = 0

for keyword in keywords:

    try:
        url = f"https://www.vinted.it/catalog?search_text={keyword}"

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a", href=True)

        found = []

        for link in links:
            href = link["href"]

            if "/items/" in href:
                full = "https://www.vinted.it" + href

                if full not in found:
                    found.append(full)

        found = found[:3]

        for item in found:

            text = f"🔭 {keyword}\n{item}"

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

            data = {
                "chat_id": CHAT_ID,
                "text": text
            }

            requests.post(telegram_url, data=data)

            sent += 1

    except Exception as e:
        print(f"Errore {keyword}: {e}")

print(f"Inviati {sent} annunci")
