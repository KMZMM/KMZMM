import telebot
import requests
import os

# Get the bot token from the environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

# CRITICAL: Point the bot to our local server running on the GitHub Actions runner
bot = telebot.TeleBot(BOT_TOKEN, api_url='http://localhost:8081')

@bot.message_handler(content_types=['document', 'video', 'photo'])
def handle_large_files(message):
    chat_id = message.chat.id
    file_info = None

    # Get the file ID based on its type
    if message.document:
        file_info = bot.get_file(message.document.file_id)
    elif message.video:
        file_info = bot.get_file(message.video.file_id)
    elif message.photo:
        # Photos are sent as an array of sizes, take the largest
        file_info = bot.get_file(message.photo[-1].file_id)

    if file_info:
        # Construct the download URL for the LOCAL server
        file_url = f'http://localhost:8081/file/bot{BOT_TOKEN}/{file_info.file_path}'
        
        # Download the file using requests
        response = requests.get(file_url)
        if response.status_code == 200:
            file_name = file_info.file_path.split('/')[-1]
            with open(file_name, 'wb') as f:
                f.write(response.content)
            bot.reply_to(message, f"I successfully downloaded your file ({file_name})! Size: {len(response.content)} bytes.")
        else:
            bot.reply_to(message, "Sorry, I couldn't download that file.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I'm running on a local server in GitHub Actions! Send me a large file (up to 2GB) and I'll try to download it.")

# Start polling (or use webhooks, but for this demo, polling is simpler)
print("Bot is starting...")
bot.infinity_polling()
