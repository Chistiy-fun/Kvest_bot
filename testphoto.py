import telebot

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')

# создаём бота
bot = telebot.TeleBot(token, parse_mode=None)


@bot.message_handler(commands=['send_photo'])
def send_photo(message):
    with open('media/Фото/location1.png', 'rb') as f:
        bot.send_photo(message.chat.id, f)


bot.infinity_polling()