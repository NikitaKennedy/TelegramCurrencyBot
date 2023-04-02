import telebot
import os
from dotenv import load_dotenv
from config import*
from GetPrise import Converter
from extensions import APIException
from telebot import types

source_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
buttons = []
for val in CURRENCY_CONVERSION.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))
source_markup.add(*buttons)
load_dotenv()
PROXY_URL = "http//proxy.server:3128"
bot = telebot.TeleBot(os.getenv("TOKEN"))

# Сообщения бота при вызове комманд /start /help
@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    text = "Для начала КАЖДОЙ НОВОЙ конвертации отправьте команду /convert\n"

    bot.reply_to(message, text)

#Процесс конвертации в формате диалога с ботом
@bot.message_handler(commands=['convert'])
def values_message(message: telebot.types.Message):
    text = "Выберите валюту из которой будете конвертировать:\n"
    bot.send_message(message.chat.id, text, reply_markup=source_markup)
    bot.register_next_step_handler(message, base_handler)
def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = "Выберите валюту в которую будете конвертировать:\n"
    bot.send_message(message.chat.id, text, reply_markup=source_markup)
    bot.register_next_step_handler(message, quote_handler, base )

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = "Выберите количество конвертируемой валюты:\n"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)
def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        result = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка ввода:\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать запрос:\n{e}")
    else:
        text = f"Перевод {amount} {base} в {quote} = {result}p."
        bot.send_message(message.chat.id, text)




bot.polling(none_stop=True, interval=0)