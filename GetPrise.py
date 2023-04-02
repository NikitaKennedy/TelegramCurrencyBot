import requests
import json
import config
from extensions import APIException
import os
from dotenv import load_dotenv

load_dotenv()

class Converter:
    @staticmethod
    # Функция принимает значения валюты, конвертируемой валюты и количество валюты
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException("Нельзя переводить валюту саму в себя")

        try:
            base = config.CURRENCY_CONVERSION[base]
        except KeyError:
            raise APIException(f"Валюта {base} не поддерживается")

        try:
            quote = config.CURRENCY_CONVERSION[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} не поддерживается")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество должно быть числом")

        if amount <= 0:
            raise APIException("Количество должно быть больше нуля")
        # Выполняем запрос API
        url = f"https://api.apilayer.com/currency_data/convert?to={quote}&from={base}&amount={amount}"
        # headers = {"apikey": f"{config.API_KEY}"} in res headers=headers os.getenv("API_KEY")
        apikey = os.getenv("API_KEY")
        headers = {"apikey": f"{apikey}"}
        payload = {}
        # Получаем ответ в формате json
        response = requests.get(url, headers=headers, data=payload)
        response_json = json.loads(response.content.decode('utf-8'))

        try:
            #Получаем цену и стоимость запрашиваемой валюты
            price = float(response_json["info"]["quote"])
            result = price * amount
            return round(result, 1,)
        except (KeyError, ValueError):
            raise APIException("Ошибка получения курса валют")


    @staticmethod
    #Возвращаем ответ в виде списка со стоимостью запрашиваемой валюты
    def get_available_currencies():
        return list(config.CURRENCY_CONVERSION.keys())

