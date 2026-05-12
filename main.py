import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

SEARCHES = [
    "telescopio",
    "cannocchiale",
    "oculare",
    "astronomia",
    "telescopio vintage",
    "accessori telescopio"
]

GOOD_WORDS = [
    "japan",
    "made in japan",
    "vintage",
    "orange",
    "fluorite",
    "ortho",
    "orthoscopic",
    "oculare",
    "astronomia",
    "c5",
    "c8",
    "vixen",
    "celestron",
    "takahashi",
    "televue",
    "pentax",
    "clavé",
    "zeiss"
]

BAD_WORDS = [
    "lego",
    "pirati",
    "bambini",
    "toy",
    "giocattolo",
    "playmobil"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

sent = 0

for search in SEARCHES:

    try:

        url = f"https://www.vinted.it/catalog?search_text={search}"

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a", href=True)

        found = []

        for link in links:

            href = link["href"]

            text = link.get_text().lower()

            if "/items/" not in href:
                continue

            if any(bad in text for bad in BAD_WORDS):
                continue

            score = 0

            for good in GOOD_WORDS:

                if good in text:
                    score += 1

            if score < 1:
                continue

            full = "https://www.vinted.it" + href

            if full not in found:
                found.append(full)

        found = found[:5]

        for item in found:

            text = f"🔭 Possibile annuncio interessante\n\n{item}"

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

            data = {
                "chat_id": CHAT_ID,
                "text": text
            }

            requests.post(telegram_url, data=data)

            sent += 1

    except Exception as e:

        print(f"Errore {search}: {e}")

print(f"Inviati {sent} annunci")
