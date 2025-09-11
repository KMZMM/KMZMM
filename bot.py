import telebot
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]  # must match your GitHub secret name
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "✅ Hello! I'm alive on GitHub Actions 🚀")

if __name__ == "__main__":
    bot.infinity_polling()

