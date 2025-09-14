import os
import requests
from pyrogram import Client
from pyrogram.types import InputMediaDocument
from telebot import TeleBot
from telebot.types import Message
import asyncio
from threading import Thread
import time

# ------------------ BOT SETUP ------------------
BOT_TOKEN = "7991946715:AAEbPVCT_MZcgIpz5nGS5SwtbtEpiIJwEOQ"  # Bot API token
bot = TeleBot(BOT_TOKEN)

# ---------------- USERBOT SETUP ----------------
USERBOT_SESSION = "user.session"  # Pyrogram session file
API_ID = 24369889  # Your API ID
API_HASH = "e5269c9b7062513f9efc5be5cd51dbd7"
UPLOAD_CHAT = "@newchkmzmm"  # Channel or group to upload movies

# Initialize Pyrogram client
userbot = Client(
    USERBOT_SESSION, 
    api_id=API_ID, 
    api_hash=API_HASH,
    no_updates=True  # Reduce overhead since we're only uploading
)

# Global variables for progress tracking
current_file = None
total_downloaded = 0
total_uploaded = 0
download_total = 0
upload_total = 0
last_progress_time = 0

# ---------------- HELPER FUNCTIONS ----------------
def download_file(url, filename, message):
    """Download file from URL with progress."""
    global total_downloaded, download_total, last_progress_time
    
    total_downloaded = 0
    r = requests.get(url, stream=True)
    download_total = int(r.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f:
        if download_total == 0:
            f.write(r.content)
        else:
            last_progress_time = time.time()
            for data in r.iter_content(chunk_size=1024*1024):
                f.write(data)
                total_downloaded += len(data)
                
                # Update progress every 2 seconds to avoid spamming
                if time.time() - last_progress_time >= 2:
                    progress = total_downloaded / download_total * 100
                    try:
                        bot.edit_message_text(
                            chat_id=message.chat.id,
                            message_id=message.message_id,
                            text=f"📥 Downloading {filename}: {progress:.1f}%"
                        )
                    except:
                        pass  # Ignore message edit errors
                    last_progress_time = time.time()

def upload_with_progress(filename, message):
    """Upload file using userbot with progress updates."""
    global total_uploaded, upload_total, last_progress_time
    
    total_uploaded = 0
    file_size = os.path.getsize(filename)
    upload_total = file_size
    last_progress_time = time.time()
    
    # Create a custom callback for progress
    def progress(current, total):
        global total_uploaded, last_progress_time
        
        total_uploaded = current
        
        # Update progress every 2 seconds to avoid spamming
        if time.time() - last_progress_time >= 2:
            progress_percent = current / total * 100
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    text=f"📤 Uploading {filename}: {progress_percent:.1f}%"
                )
            except:
                pass  # Ignore message edit errors
            last_progress_time = time.time()
    
    # Run the upload in the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    with userbot:
        try:
            userbot.send_document(
                UPLOAD_CHAT, 
                filename,
                progress=progress
            )
            return True
        except Exception as e:
            print(f"Upload error: {e}")
            return False

# ---------------- BOT HANDLER ----------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Send me a direct download link, and I will upload it to Telegram!")

@bot.message_handler(func=lambda msg: True)
def handle_link(message):
    url = message.text.strip()
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        bot.reply_to(message, "❌ Please provide a valid HTTP/HTTPS URL")
        return
    
    # Extract filename from URL or use default
    filename = os.path.basename(url) or "file.bin"
    
    # Check if the filename has an extension
    if '.' not in filename:
        filename += '.mp4'  # Default to mp4 if no extension
    
    # Send initial message
    status_msg = bot.reply_to(message, f"📥 Downloading {filename}...")
    
    try:
        # Download the file
        download_file(url, filename, status_msg)
        
        # Check if download was successful
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text="❌ Download failed or file is empty"
            )
            return
        
        # Update status to uploading
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            text=f"📤 Uploading {filename} to Telegram..."
        )
        
        # Upload the file
        success = upload_with_progress(filename, status_msg)
        
        if success:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=f"✅ {filename} uploaded successfully to {UPLOAD_CHAT}!"
            )
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=f"❌ Failed to upload {filename}"
            )
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=error_msg
            )
        except:
            bot.reply_to(message, error_msg)
    
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)

# Initialize userbot session
def init_userbot():
    try:
        with userbot:
            print("Userbot session ready.")
    except Exception as e:
        print(f"Userbot initialization failed: {e}")

# ---------------- START BOT ----------------
if __name__ == "__main__":
    print("Initializing userbot session...")
    init_userbot()
    
    print("Bot is running...")
    bot.infinity_polling()