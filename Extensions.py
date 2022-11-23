import requests
from Config import currency_list


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Конвертация {base} в {base} невозможна.')

        try:
            base_ticker = currency_list[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({base}).')

        try:
            quote_ticker = currency_list[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({quote}).')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество ({amount}).')

        r = requests.get(
            f'https://api.apilayer.com/currency_data/convert?apikey=6w5iMfp9l8jnWgjEOHcrp68iRIentrod&to={quote_ticker}&from={base_ticker}&amount={amount}').json()
        total_quote = r['result']
        return total_quote
