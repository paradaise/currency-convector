import telebot
from telebot import types
from api_tokens import TG_API_TOKEN
from api_tokens import CONVERT_API_TOKEN
import re
import requests

api_url = f'https://v6.exchangerate-api.com/v6/{CONVERT_API_TOKEN}/latest/'
bot = telebot.TeleBot(TG_API_TOKEN)
main_menu = ('📑Контакты', '💸Поддержать','📖Наименование валют')
donation_menu = ('🫰Юмани', '💰СБП', '↩️Назад')

def keyboard(menu):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in menu:
        markup.add(types.KeyboardButton(item))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    name = message.from_user.first_name
    bot.reply_to(message, f'<i>Привет,<b>{name} AKA {username}</b>!Я бот валютный конвектор!Напиши выражение вида:</i> <b>[int] [VAL1] в [VAL2] </b> \n<i>Пример:\n</i> <b>200 RUB в USD</b>', 
            reply_markup=keyboard(main_menu), parse_mode="html")
    
    send_document(message)
    


@bot.message_handler(content_types=['text'])
def get_information(message):
    if message.chat.type == 'private':
        if message.text == '📑Контакты':
            bot.send_message(message.chat.id,'У вас что-то не работает?Или есть предложения о сотрудничестве?Напишите мне!')
            bot.send_message(message.chat.id,'Гоголев Виктор:\n📱Telegram: t.me/wa55up\n🌐Вконтакте: vk.com/yowa55up\n🐙GitHub: github.com/paradaise\n')
        elif message.text == '💸Поддержать':
            bot.send_message(message.chat.id,'💵Вы можете поддержать наш проект,нажав кнопку ниже:', reply_markup = keyboard(donation_menu))
        elif message.text == '🫰Юмани':
            bot.send_message(message.chat.id,'🫰Вы можете поддержать Юмани по ссылке:\nhttps://yoomoney.ru/to/410013032669115')
        elif message.text == '💰СБП':
            bot.send_message(message.chat.id,'💰Вы можете поддержать CБП по ссылке:')
        elif message.text == '↩️Назад':
            bot.send_message(message.chat.id,'↩️Возвращаемся к основному меню', reply_markup = keyboard(main_menu))
        elif message.text == '📖Наименование валют':
            bot.send_message(message.chat.id,'<i>Вот список актуальных валют!:</i>',parse_mode="html")
            
            send_document(message)


        else:
            print(message.text)
            words = message.text.split()
            pattern = r"^\d+ [A-Z]{3} в [A-Z]{3}$"

            if len(words) == 4  and re.match(pattern, message.text) and words[1] != words[3]:
                amount = float(words[0])
                from_currency = words[1]
                to_currency = words[3]
                convert_currency(message, amount, from_currency, to_currency)
            else:
                bot.send_message(message.chat.id, f'<i>Сообщение не корректно,напишите согласно шаблона:</i> \n<b> [int] [VAL1] в [VAL2] </b>\n <i>Пример:</i>\n <b>200 RUB в USD</b> ', parse_mode='HTML')




def convert_currency( message, amount = 100, from_currency = 'RUB', to_currency = 'USD'):
    r = requests.get(f"{api_url}{from_currency}")
    if r.status_code == 200:
        if (from_currency and to_currency) in r.json()['conversion_rates']:
            current_cource = r.json()['conversion_rates'][to_currency]
            answer = amount * current_cource
            bot.send_message(message.chat.id, f'<i>Мы все посчитали😎:</i> <b><i>{amount} {from_currency}</i></b> это <i><b>{answer:.4f} {to_currency}</b></i>', parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, f"<i>Произошла ошибка ввода, вы ввели не существующую валюту.\nПопробуйте изменить запрос соглазно валютам из списка!</i>",parse_mode="html")
    else:
        bot.send_message(message.chat.id, f"<i>Произошла ошибка запроса, скорее всего ошибка в API.\nПопробуйте обратиться позже!\nОшибка:</i><b>{r.status_code}</b>",parse_mode="html")

def send_document(message):
    document = open('currency_info.txt','rb')
    bot.send_document(message.chat.id, document)


bot.polling(none_stop=True)
