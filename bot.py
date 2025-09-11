import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)

HEADERS = {
    "user-agent": "Dart/3.7 (dart:io)",
    "accept-encoding": "gzip",
    "content-type": "application/json",
    "authorization": os.environ["AUTH_TOKEN"]  # Add AUTH_TOKEN as GitHub secret
}

SEARCH_URL = "https://or.smstv.live/api/sub/movie/search"
SOURCE_URL = "https://or.smstv.live/api/sub/movie/source/get/{}"

# --------- API Functions ---------
def search_movies(keyword):
    try:
        r = requests.post(SEARCH_URL, headers=HEADERS, json={"movie_name": keyword}, timeout=10)
        r.raise_for_status()
        return r.json().get("data", [])
    except:
        return []

def fetch_movie_sources(movie_id):
    try:
        r = requests.get(SOURCE_URL.format(movie_id), headers=HEADERS, timeout=10)
        r.raise_for_status()
        sources_node = r.json().get("data", [])
        return [{"name": src.get("source_name"), "url": src.get("url")} for src in sources_node]
    except:
        return []

# --------- Telegram Handlers ---------
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello! Send me a movie name and I will search it for you.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    keyword = message.text.strip()
    msg = bot.send_message(message.chat.id, f"Searching for '{keyword}'...")
    
    movies = search_movies(keyword)
    if not movies:
        bot.edit_message_text("No movies found.", chat_id=message.chat.id, message_id=msg.message_id)
        return

    bot.edit_message_text(f"Found {len(movies)} movies.", chat_id=message.chat.id, message_id=msg.message_id)

    for movie in movies:
        movie_id = movie.get("id")
        name = movie.get("name")
        poster = movie.get("poster")  # URL of poster
        description = movie.get("description", "")
        sources = fetch_movie_sources(movie_id)

        markup = InlineKeyboardMarkup()
        for src in sources:
            if src["url"]:
                markup.add(InlineKeyboardButton(f"Watch: {src['name']}", url=src["url"]))

        caption = f"<b>{name}</b>\n\n{description[:300]}"  # first 300 chars
        try:
            bot.send_photo(chat_id=message.chat.id, photo=poster, caption=caption, parse_mode="HTML", reply_markup=markup)
        except:
            bot.send_message(chat_id=message.chat.id, text=caption, parse_mode="HTML", reply_markup=markup)

# --------- Run Bot ---------
if __name__ == "__main__":
    bot.infinity_polling()


