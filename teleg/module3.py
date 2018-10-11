import telebot
import flightradar24

TOKEN = '522692515:AAFfvs7tagT6jhNob7sLs0SyyL9Xew-Fl_E'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    start_menu = bot.send_message(message.chat.id, '{}, добро пожаловать.'.format(message.from_user.first_name))
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('AFL', 'PBD', 'FIN')
    markup.row('UAE', 'QTR', 'KAL')
    markup.row('SIA', 'KZR', 'THY')
    global sentavia
    sentavia = bot.send_message(message.chat.id, 'Введите код авиакомпании ICAO?', reply_markup=markup)
    bot.register_next_step_handler(sentavia, av)


def av(message):

    airline = message.text.upper()
    fr = flightradar24.Api()
    flights = fr.get_flights(airline)
    l = len(list(flights.values()))
    k = list(flights.values())[2:l-1]
    if k != []:
        for i in k:
            bot.send_message(message.chat.id,'рейс - {}, типа самолета - {}, {}->{}, высота - {}м, скорость - {}км/ч'.format(i[13],i[8], i[11], i[12], round(i[4]*0.3048), round(i[5]*1.852)))
        bot.send_message(message.chat.id, 'всего найдено рейсов - {}'.format(len(k)))
        bot.send_message(message.chat.id, 'готово')
        bot.send_message(message.chat.id, 'Введите вновь код авиакомпании ICAO?')
    else:
        bot.send_message(message.chat.id, 'Не корректный запрос. Попробуйте снова.')
    bot.register_next_step_handler(sentavia, av)



bot.polling(none_stop=True)