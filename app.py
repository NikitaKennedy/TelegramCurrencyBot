import telebot
import config
from GetPrise import Converter
from extensions import APIException
bot = telebot.TeleBot(config.TOKEN)
# Сообщения бота при вызове комманд /start /help
@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    text = "Для получения цены на валюту, отправьте сообщение в формате:\n<имя валюты> <в какую валюту перевести> <количество>\n" \
           "Пример ввода: USD RUB 10 -> Ответ: Перевод 10 USD в RUB = 765.35р. \n" \
           "Для получения списка доступных валют, отправьте команду /values\n"

    bot.reply_to(message, text)

#Сообщение бота с доступными валютами при вызове комманды /value
@bot.message_handler(commands=['values'])
def values_message(message):
    text = "Доступные валюты:\n"
    for val in Converter.get_available_currencies():
        text += val + '\n'
    bot.reply_to(message, text)

#Ответ бота на заброс конвертации валют
@bot.message_handler(content_types=['text'])
def convert_message(message):
    try:
        base, quote, amount = message.text.split(' ')
        result = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка ввода:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать запрос:\n{e}")
    else:
        text = f"Перевод {amount} {base} в {quote} = {result}"
        bot.reply_to(message, text)


bot.polling(none_stop=True, interval=0)