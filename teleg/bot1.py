from random import randint
import telebot

TOKEN = '660998626:AAHgAzbMgxUhhLA8dlcb7u192Az5FCeWnpM'
bot = telebot.TeleBot(TOKEN)
words = ['подтверждаю', 'угу', 'не подтверждаю']
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '{}, здравствуйте. Это бот, который что-то подтверждает. Напишите что-то'.format(message.from_user.first_name))


@bot.message_handler(func=lambda message: True)
def begin(message):
    bot.send_message(message.chat.id, words[randint(0,len(words)-1)])



while True:
    try:
        bot.infinity_polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)