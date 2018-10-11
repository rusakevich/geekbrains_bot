from google.cloud import bigquery
import os
import telebot


TOKEN = '382553820:AAGX_FIF73-aVCQ2BadKV96zlVMSxCqekoI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    start_menu = bot.send_message(message.chat.id, '{}, добро пожаловать.'.format(message.from_user.first_name))
    global question
    question = bot.send_message(message.chat.id, 'Введите диапозон дат в формате - ГГГГ-ММ-ДД ГГГГ-ММ-ДД?')
    bot.register_next_step_handler(question, funnels)



def funnels(message):
    if len(message.text) == 21:
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/v_rusakevich/Documents/Виджеты power bi/Yolla-d505c9833f92.json'
            client = bigquery.Client()
            v = 'enter_phone'
            QUERY = ('select * from (SELECT COUNT(name) AS c, '
            '"Открытие первого экрана" as s '
            'FROM ( ' 
             'SELECT "ANDROID" AS OS, ' 
              'user_dim.user_id, '
              'cast (TIMESTAMP_MICROS(event.timestamp_micros) as date) as dates, '
              'event.name '
              'FROM  `yolla-33cfc.com_yollacalls_ANDROID.app_events_201*`, UNNEST(event_dim) AS event '
              'WHERE event.name = "tutorial_begin") '
              'WHERE dates between @dates1 and @dates2 '

               'UNION ALL '
 
               'SELECT COUNT(name) AS c, '
               '"Введен валидный номер" as s '
              'FROM ( ' 
              'SELECT "ANDROID" AS OS, '
              'user_dim.user_id, '
              'cast (TIMESTAMP_MICROS(event.timestamp_micros) as date) as dates, '
              'event.name '
              'FROM  `yolla-33cfc.com_yollacalls_ANDROID.app_events_201*`, UNNEST(event_dim) AS event '
              'WHERE event.name = "enter_phone") '
               'WHERE dates between @dates1 and @dates2 '
      
               'UNION ALL '
 
               'SELECT COUNT(name) AS c,'
               '"Успешная регистрация" as s '
              'FROM ( ' 
              'SELECT "ANDROID" AS OS, '
              'user_dim.user_id, '
              'cast (TIMESTAMP_MICROS(event.timestamp_micros) as date) as dates, '
              'event.name '
              'FROM  `yolla-33cfc.com_yollacalls_ANDROID.app_events_201*`, UNNEST(event_dim) AS event '
              'WHERE event.name = "sign_up") '
               'WHERE dates between @dates1 and @dates2) '
               'order by c desc '
            )


            d1 = message.text[0:10]
            d2 = message.text[11:21]
            param1 = bigquery.ScalarQueryParameter('dates1', 'STRING', d1)
            param2 = bigquery.ScalarQueryParameter('dates2', 'STRING', d2)

            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = [param1, param2]

            query_job = client.query(QUERY, job_config=job_config) 

            rows = query_job.result()
            for row in rows:
                bot.send_message(message.chat.id, '{} - {}'.format(row.s, row.c))
            bot.send_message(message.chat.id, 'Введите новые даты?')
            bot.register_next_step_handler(question, funnels)

        except:
            bot.send_message(message.chat.id, 'Некорректные даты! Попробуйте снова ввести в формате - ГГГГ-ММ-ДД ГГГГ-ММ-ДД?')
            bot.register_next_step_handler(question, funnels)

    else:
        bot.send_message(message.chat.id, 'Некорректные даты! Попробуйте снова ввести в формате - ГГГГ-ММ-ДД ГГГГ-ММ-ДД?')
        bot.register_next_step_handler(question, funnels)
bot.polling(none_stop=True)