from google.cloud import bigquery
import os
import telebot


TOKEN = '382553820:AAGX_FIF73-aVCQ2BadKV96zlVMSxCqekoI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    start_menu = bot.send_message(message.chat.id, '{}, добро пожаловать.'.format(message.from_user.first_name))
    global question
    question = bot.send_message(message.chat.id, 'Введите диапозон дат регистраций - ГГГГ-ММ-ДД ГГГГ-ММ-ДД?')
    bot.register_next_step_handler(question, funnels)

def funnels(message):
    if len(message.text) == 21:
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/v_rusakevich/Documents/Виджеты power bi/Yolla-d505c9833f92.json'
            client = bigquery.Client()
            QUERY =(
                'with t1 as '
            '(SELECT '
              'S.user_id, '
              'cast(TIMESTAMP_MICROS(S.timestamp_micros) as date) AS time_register, '
              'cast(TIMESTAMP_MICROS(P.timestamp_micros) as date) AS time_purchase, '
               'CASE '
                'WHEN (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) <=0 THEN "Меньше 0" '
                'WHEN (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) > 0 and (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) <=86400000000 THEN "меньше суток" '
                'WHEN (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) > 86400000000 and (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) <=604800000000 THEN "1сутки < Time < 1нед" '
                'WHEN (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) > 604800000000 and (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) <=2592000000000 THEN "1нед < Time < 30дней" '
                'WHEN (CAST(P.timestamp_micros AS int64) - CAST(S.timestamp_micros AS int64)) > 2592000000000 THEN "Time > 30дней" '
                'else "Не определено" '
              'END time_segment_max '
            'FROM ( '
              'SELECT * '
              'FROM ( '
               'SELECT '
                  'user_dim.user_id, '
                  'event.name, '
                  'event.timestamp_micros, '
                  'event.previous_timestamp_micros, '
                  'ROW_NUMBER() OVER(PARTITION BY user_dim.user_id ORDER BY event.timestamp_micros) AS rangs '
                'FROM `yolla-33cfc.com_yollacalls_ANDROID.app_events_201*`, '
                  'UNNEST(event_dim) AS event '
                'WHERE event.name="sign_up") '
              'WHERE rangs=1) AS S '
            'INNER JOIN ( '
              'SELECT * '
              'FROM ( '
                'SELECT '
                  'user_dim.user_id, '
                  'event.name, '
                  'event.timestamp_micros, '
                  'event.previous_timestamp_micros, '
                  'ROW_NUMBER() OVER(PARTITION BY user_dim.user_id ORDER BY event.timestamp_micros) AS rangs '
                'FROM `yolla-33cfc.com_yollacalls_ANDROID.app_events_201*`, '
                  'UNNEST(event_dim) AS event '
                'WHERE  event.name="ecommerce_purchase") '
              'WHERE rangs = 1) AS P '
            'ON '
             'S.user_id=P.user_id) '
  

 
             '(select count(user_id) as amount, round(count(user_id)/(select count(user_id) from t1 where time_register between @dates1 and @dates2)*100,2) as proc,"Меньше 0" as segm from t1 where time_segment_max = "Меньше 0" and time_register between @dates1 and @dates2 '
             'union all '
             'select count(user_id) as amount, round(count(user_id)/(select count(user_id) from t1 where time_register between @dates1 and @dates2)*100,2) as proc,"меньше суток" as segm from t1 where time_segment_max = "меньше суток" and time_register between @dates1 and @dates2 '
             'union all '
             'select count(user_id) as amount, round(count(user_id)/(select count(user_id) from t1 where time_register between @dates1 and @dates2)*100,2) as proc,"1сутки < Time < 1нед" as segm from t1 where time_segment_max = "1сутки < Time < 1нед" and time_register between @dates1 and @dates2 '
             'union all '
             'select count(user_id) as amount, round(count(user_id)/(select count(user_id) from t1 where time_register between @dates1 and @dates2)*100,2) as proc,"1нед < Time < 30дней" as segm from t1 where time_segment_max = "1нед < Time < 30дней" and time_register between @dates1 and @dates2 '
             'union all '
             'select count(user_id) as amount, round(count(user_id)/(select count(user_id) from t1 where time_register between @dates1 and @dates2)*100,2) as proc,"Time > 30дней" as segm from t1 where time_segment_max = "Time > 30дней" and time_register between @dates1 and @dates2) '
              'order by amount desc  '
              )

            d1 = message.text[0:10]
            d2 = message.text[11:21]
            param1 = bigquery.ScalarQueryParameter('dates1', 'STRING', d1)
            param2 = bigquery.ScalarQueryParameter('dates2', 'STRING', d2)

            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = [param1, param2]

            query_job = client.query(QUERY, job_config=job_config) 

            rows = query_job.result()
            S = 0
            for row in rows:
                bot.send_message(message.chat.id, '{} — {}% — {}'.format(row.segm, row.proc, row.amount))
                S += row.amount
            bot.send_message(message.chat.id, 'Всего за этот период осуществлено {} первых платежей'.format(S))
            bot.send_message(message.chat.id, 'Введите новые даты?')
            bot.register_next_step_handler(question, funnels)

        except:
            bot.send_message(message.chat.id, 'Некорректные даты! Попробуйте снова ввести в формате - ГГГГ-ММ-ДД ГГГГ-ММ-ДД?')
            bot.register_next_step_handler(question, funnels)

    else:
        bot.send_message(message.chat.id, 'Некорректные даты! Попробуйте снова ввести в формате - ГГГГ-ММ-ДД ГГГГ-ММ-ДД?')
        bot.register_next_step_handler(question, funnels)


bot.polling(none_stop=True)