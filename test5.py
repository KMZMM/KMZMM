import os
import requests
from pyrogram import Client
from telebot import TeleBot

# ------------------ BOT SETUP ------------------
BOT_TOKEN = "7991946715:AAEbPVCT_MZcgIpz5nGS5SwtbtEpiIJwEOQ"      # Bot API token
bot = TeleBot(BOT_TOKEN)

# ---------------- USERBOT SETUP ----------------
USERBOT_SESSION = "user.session"  # Pyrogram session file
API_ID = 24369889                   # Your API ID
API_HASH = "e5269c9b7062513f9efc5be5cd51dbd7"
UPLOAD_CHAT = "@newchkmzmm"  # Channel or group to upload movies

# Initialize Pyrogram client
userbot = Client(USERBOT_SESSION, api_id=API_ID, api_hash=API_HASH)

# ---------------- HELPER FUNCTIONS ----------------
def download_file(url, filename):
    """Download file from URL with progress."""
    r = requests.get(url, stream=True)
    total = r.headers.get('content-length')
    with open(filename, 'wb') as f:
        if total is None:
            f.write(r.content)
        else:
            downloaded = 0
            total = int(total)
            for data in r.iter_content(chunk_size=1024*1024):
                f.write(data)
                downloaded += len(data)
                print(f"Downloading {filename}: {downloaded/1024/1024:.2f} MB / {total/1024/1024:.2f} MB")

def upload_file(filename):
    """Upload file using userbot."""
    with userbot:
        userbot.send_document(UPLOAD_CHAT, filename)
        print(f"Uploaded {filename} successfully!")

# ---------------- BOT HANDLER ----------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Send me a direct download link, and I will upload it to Telegram!")

@bot.message_handler(func=lambda msg: True)
def handle_link(message):
    url = message.text.strip()
    filename = url.split("/")[-1] or "file.mp4"
    bot.reply_to(message, f"Downloading {filename}...")
    try:
        download_file(url, filename)
        bot.reply_to(message, f"Uploading {filename} to Telegram...")
        upload_file(filename)
        bot.reply_to(message, f"✅ {filename} uploaded successfully!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)  # Remove file after upload

# ---------------- START BOT ----------------
if __name__ == "__main__":
    print("Bot is running...")
    # First-time userbot login will ask OTP if session does not exist
    with userbot:
        print("Userbot session ready.")
    bot.infinity_polling()