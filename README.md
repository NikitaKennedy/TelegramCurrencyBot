# TelegramCurrencyBot @EasyCurrencyBot
Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
Бот использует API запрос к сайту apilayer.com
Добавлять валюты можно в файле config.py обозначения валют должны соответсвовать международным стандратам (например Доллар США = USD)
В файле main.py находится код бота (использована билиотека pytelegrambotapi)
В файле gGetPrise.py класс обработки и конвертации валют
В файле extensions.py исключения для обработки ошибок( хотя, как мне кажетстя он здесь лишний)
В файле config.py список доступных валют
