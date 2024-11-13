import telebot
import requests
import json
from config import keys, TOKEN
from extentions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = "Для начала работы введите запрос в следующем формате (через пробел):" \
            " \n- Название первой валюты, из которой Вы хотите конвертировать \n- Название второй валюты, в которую " \
            "Вы хотите конвертировать \n- Сумму денег в первой валюте \n \n Например: \n рубль евро 100 \n \n " \
            "Для просмотра списка доступных валют нажмите: /currency"
    bot.reply_to(message, text)


@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        message.text = ' '.join(message.text.split()) #Удаление из строки лишних пробелов
        values = message.text.split(' ')
        if len(values) != 3 :
            raise APIException('Неверно введен запрос')
        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка\n{e}')
    else:
        text = f'{amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)