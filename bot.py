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
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZWJjNDUzZS00ZTU5LTRiOGEtYjk0Ny0xMWUwNjUyN2NhZDUiLCJqdGkiOiI0NzdhMzUyYWMwOGVhYWNiMDNiNTNmYzhkY2FmMTQ4YmQ2MWMwNTZhMDcwY2Y2MzJmMWFhYzI5OTQ5MWNjMDE5YzIyZDk3YTQwNGFiOTE2YiIsImlhdCI6MTc1NzQ5OTIxNy40NjQwOTYsIm5iZiI6MTc1NzQ5OTIxNy40NjQxMDQsImV4cCI6MTc4OTAzNTIxNy40NTEyMjEsInN1YiI6IjE3MDkiLCJzY29wZXMiOltdfQ.fHLgsxcD-zvdxWF0tvlW2zZzrQvXTGrcrKkBf1_HkyWYEoKE_Vu13_nVt9BUJQhgeJyN5vj-9rPnWIJmOfjFDaxJODxHuQ3xxHvKi80GBDz7MypXRfMaH0QYcVYGYCnoesL0oOMOuya55NNWF2R5wqlxS7n5CjHHwqbgiV0HQ3qqZn1ifZasLDiS8dufflDDrQoCHj_gHOSg8IHgWQEprrBh-jgH83KdtZkhM7JdXudKF4K_JZycD9u7sCtMRbWqRYCqMiwWD91n2A8dpPgzChsMVB3nLBtCnsI-hRVptq9phunfDK13GtvPiKPTVwnLTWH5TpXgqqTPeYXGdbodbETsIo9AC6f02lWuczXOW2kjKHKXcOxAQnEN4J7unvnuI5Gm_zmbebTzmbOwH2HuanYsEJlmw7cUh52mek2DWBQFXSqg_iKt5DaiCSL8eM20fVDH3PNpgHhadolGgL0msSvdUscSUbLnpU2ekVJZcQwviLM0IkKXih7cPIXgQV2EuUUN09bR4mQvb7H2S3TFXwzs6QUpDv8F10vn0VBsFx9rRqkdT_y7b45XB8XcCYvCCEVkDa6rrx_W343xNQ4HLboVVQkn-wEKMXaNzpoKcdmOrU3sbT169ybt_U-nqAs_YY1MC-o1GknSBeU6nrWUjIb2cIyee8oGu_fkLdTB-gk"  # Add AUTH_TOKEN as GitHub secret
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


