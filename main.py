import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

SEARCHES = [
    "telescopio",
    "teleskop",
    "cannocchiale",
    "oculare",
    "astronomia",
    "telescopio vintage"
]

BAD_SIGNALS = [
    "lego",
    "toy",
    "playmobil",
    "pirati",
    "bambini",
    "kids",
    "clementoni",
    "20x",
    "30x",
    "40x",
    "50x",
    "60x",
    "90x",
    "120x",
    "hd telescope",
    "smartphone telescope",
    "national geographic",
    "bresser junior",
    "science kit",
    "educational",
    "giocattolo",
    "mobile",
    "ingranditore",
    "monocolo",
    "libro"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

with open("marketplace_seen.txt", "r") as f:
    seen = f.read().splitlines()

new_seen = seen.copy()

sent = 0

MARKETPLACES = [
    ("Vinted", "https://www.vinted.it/catalog?search_text={}"),
    ("Subito", "https://www.subito.it/annunci-italia/vendita/usato/?q={}"),
    ("Wallapop", "https://it.wallapop.com/app/search?keywords={}")
]

for marketplace_name, marketplace_url in MARKETPLACES:

    for search in SEARCHES:

        try:

            url = marketplace_url.format(search.replace(" ", "%20"))

            r = requests.get(url, headers=headers, timeout=15)

            soup = BeautifulSoup(r.text, "html.parser")

            links = soup.find_all("a", href=True)

            for link in links:

                href = link["href"]

                text = link.get_text().lower()

                if any(bad in text for bad in BAD_SIGNALS):
                    continue

                if marketplace_name == "Vinted":

                    if "/items/" not in href:
                        continue

                    full_link = "https://www.vinted.it" + href

                elif marketplace_name == "Subito":

                    if "/annuncio/" not in href:
                        continue

                    full_link = href

                else:

                    if "wallapop.com/item" not in href:
                        continue

                    full_link = href

                if full_link in seen:
                    continue

                message = f"""
🔭 Nuovo annuncio discovery

🌍 Marketplace: {marketplace_name}

🔎 Ricerca: {search}

🔗 {full_link}
"""

                telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

                data = {
                    "chat_id": CHAT_ID,
                    "text": message
                }

                requests.post(telegram_url, data=data)

                new_seen.append(full_link)

                sent += 1

                if sent >= 10:
                    break

        except Exception as e:

            print(f"Errore {marketplace_name} {search}: {e}")

with open("marketplace_seen.txt", "w") as f:

    for item in new_seen:
        f.write(item + "\n")

print(f"Inviati {sent} nuovi annunci")
