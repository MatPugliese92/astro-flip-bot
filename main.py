import os
import requests

TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

KEYWORDS = [
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

sent_items = []

for keyword in KEYWORDS:

    url = f"https://www.vinted.com/api/v2/catalog/items?search_text={keyword}"

    try:

        response = requests.get(url, headers=headers)

        data = response.json()

        items = data.get("items", [])

        for item in items[:3]:

            title = item.get("title", "No title")

            price = item.get("price", "0")

            item_url = item.get("url", "")

            item_id = item.get("id")

            if item_id in sent_items:
                continue

            message = f"""
🔭 Nuovo annuncio Vinted

{title}

💰 {price} €

🔗 https://www.vinted.com{item_url}
"""

            telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

            requests.post(
                telegram_url,
                data={
                    "chat_id": CHAT_ID,
                    "text": message
                }
            )

            sent_items.append(item_id)

            print(f"Inviato: {title}")

    except Exception as e:

        print(f"Errore keyword {keyword}: {e}")

print("Controllo completato")
