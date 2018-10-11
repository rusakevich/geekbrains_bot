from google.cloud import bigquery
import os
import telebot

TOKEN = '688421952:AAGhx0qmOJ9v64Rwt-QhsMYlVlhVnLdh4eI'
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    start_menu = bot.send_message(message.chat.id, '{}, добрый день'.format(message.from_user.first_name))
    global question
    question = bot.send_message(message.chat.id, 'Введите дату ГГГГММДД')
    bot.register_next_step_handler(question, country)

def country(message):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/v_rusakevich/Documents/Виджеты power bi/Yolla-d505c9833f92.json'
    client = bigquery.Client()
    QUERY = (
    'select p.country, count(distinct p.user_pseudo_id) as volume '
    'from (SELECT geo.country,user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "ecommerce_purchase" and event_date = @dates) as p '
    'inner join '
    '(SELECT user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "first_open" and event_date = @dates) as f on p.user_pseudo_id = f.user_pseudo_id '
    'group by p.country '
    'order by volume desc ')

    param = bigquery.ScalarQueryParameter('dates', 'STRING', message.text)

    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = [param]

    query_job = client.query(QUERY, job_config=job_config) 

    rows = query_job.result()
    for row in rows:
        bot.send_message(message.chat.id, '{} - {}'.format(row.country , row.volume))
        print(row.country)





bot.polling(none_stop=True)