import telebot
from telebot import types
from game import Game
import json
# Загружаем данные о локациях из файла JSON
with open('game.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Создаем бота
bot = telebot.TeleBot('6608340726:AAFVQSnbdl9ZcmbwWxUrPIXnHqHcyk4B2L4')

# Словарь для отслеживания текущей игры для каждого пользователя
game_dict = {}


def load_user_data():
    try:
        with open('user_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}

def save_user_data():
    with open('user_data.json', 'w', encoding='utf-8') as file:
        json.dump(users_data, file, ensure_ascii=False, indent=4)

users_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    game_dict[user_id] = Game(data)
    bot.send_message(user_id, game_dict[user_id].start_game(), reply_markup=create_keyboard())

# Обработчик inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    response = game_dict[user_id].process_input(call.data)
    bot.send_message(user_id, response, reply_markup=create_keyboard())

# Функция для создания клавиатуры с вариантами ответов
def create_keyboard():
    user_id = call.from_user.id
    options = game_dict[user_id].current_location['options']
    keyboard = types.InlineKeyboardMarkup()
    for key, value in options.items():
        keyboard.add(types.InlineKeyboardButton(text=key, callback_data=key))
    return keyboard

# Запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
