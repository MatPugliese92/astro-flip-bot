import requests
from bs4 import BeautifulSoup
import telegram
import os

TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

bot = telegram.Bot(token=TOKEN)

KEYWORDS = {
    "Nagler": 200,
    "Ethos": 500,
    "Pentax XW": 220,
    "C8": 700
}

for keyword, max_price in KEYWORDS.items():

    url = f"https://www.ebay.it/sch/i.html?_nkw={keyword}"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.select(".s-item")

    for item in items[:5]:

        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        link = item.select_one(".s-item__link")

        if not title or not price or not link:
            continue

        try:
            price_value = float(
                price.text
                .replace("EUR", "")
                .replace("€", "")
                .replace(".", "")
                .replace(",", ".")
                .split(" ")[0]
            )
        except:
            continue

        if price_value <= max_price:

            message = f"""
🔥 OCCASIONE

{title.text}

💰 Prezzo: {price_value}€

🎯 Sotto soglia: {max_price}€

🔗 {link['href']}
"""

            bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

            break
