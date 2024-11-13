import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось определить валюту: {base}')
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось определить валюту: {quote}')
        if quote.lower() == base.lower():
            raise APIException(f'Введены одинаковые валюты: {base}, {quote}')
        try:
            amount = float(amount.replace(',', '.'))  #Замена запятой на точку перед преобразованием строки в число
        except ValueError:
            raise APIException(f'Неверно введена сумма: {amount}')
        if amount < 0:
            raise APIException(f'Введена отрицательная сумма: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(amount / json.loads(r.content)[keys[base.lower()]], 5)
        return total_base



