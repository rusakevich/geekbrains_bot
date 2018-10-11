import telebot

TOKEN = '688421952:AAGhx0qmOJ9v64Rwt-QhsMYlVlhVnLdh4eI'
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(content_types=['contact'])
def start(message):
    print(contact.phone_number)


bot.polling(none_stop=True)
