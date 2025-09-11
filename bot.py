import telebot
import os

BOT_TOKEN = os.environ["7256834308:AAH-YzGauoYaMQsnRNxbqG7FutO9FjcM6ac"]
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello! I'm alive on GitHub Actions 😎")

bot.infinity_polling()
