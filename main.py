import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

SEARCHES = [
    "telescopio",
    "cannocchiale",
    "oculare",
    "astronomia"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

GOOD_WORDS = [
    "japan",
    "vintage",
    "orange",
    "fluorite",
    "ortho",
    "c5",
    "c8",
    "vixen",
    "celestron",
    "takahashi",
    "televue",
    "pentax",
    "zeiss"
]

BAD_WORDS = [
    "lego",
    "toy",
    "playmobil",
    "pirati",
    "bambini"
]

with open("sent_items.txt", "r") as f:
    sent_items = f.read().splitlines()

new_sent_items = sent_items.copy()

sent = 0

for search in SEARCHES:

    try:

        url = f"https://www.vinted.it/catalog?search_text={search}"

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a", href=True)

        for link in links:

            href = link["href"]

            text = link.get_text().lower()

            if "/items/" not in href:
                continue

            full_link = "https://www.vinted.it" + href

            if full_link in sent_items:
                continue

            if any(bad in text for bad in BAD_WORDS):
                continue

            score = 0

            for good in GOOD_WORDS:

                if good in text:
                    score += 1

            if score >= 2:
                level = "🔴 MOLTO interessante"
            elif score == 1:
                level = "🟡 Interessante"
            else:
                level = "🟢 Da controllare"

            message = f"""
{level}

🔭 Ricerca: {search}

🔗 {full_link}
"""

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

            data = {
                "chat_id": CHAT_ID,
                "text": message
            }

            requests.post(telegram_url, data=data)

            new_sent_items.append(full_link)

            sent += 1

            if sent >= 10:
                break

    except Exception as e:

        print(f"Errore {search}: {e}")

with open("sent_items.txt", "w") as f:

    for item in new_sent_items:
        f.write(item + "\n")

print(f"Inviati {sent} nuovi annunci")
