import telebot
from Config import currency_list, TOKEN
from Extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def tip(message: telebot.types.Message):
    text = 'Для конвертации введите исходную валюту, валюту, в которую необходимо конвертировать, \
и сумму (например, доллар рубль 3) \
\nЧтобы увидеть все доступные валюты, введите команду: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currencies(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency_list.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        if len(values) < 3:
            raise APIException('Недостаточно параметров.')

        quote, base, amount = values

        total_quote = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\nОшибка: {e}')
    else:
        text = f'{amount} {quote} = {total_quote} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
