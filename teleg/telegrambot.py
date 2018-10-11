from datetime import date, timedelta
from google.cloud import bigquery
import os
import telebot

TOKEN = '688421952:AAGhx0qmOJ9v64Rwt-QhsMYlVlhVnLdh4eI'
bot = telebot.TeleBot(TOKEN)
users = ['OtetsFedor','rusakevich_v', 'jjjj']


gplay = ('select case when Country is null then "TOTAL" else Country end as Country, '
        'store, Installers, Conversion, One_day from (SELECT Country, SUM(Store_Listing_Visitors) AS store, '
        'SUM(Installers) AS Installers, '
        'concat(cast(ROUND(SUM(Installers)/SUM(Store_Listing_Visitors)*100,1) as string),"%")  AS Conversion, '
        'SUM(Installers_retained_for_1_day) AS One_day '
        'FROM `yolla-33cfc.com_yollacalls_ANDROID.p_Retained_installers_country_Yolla` '
        'WHERE date = @dates '
        'GROUP BY ROLLUP(Country)) '
        'ORDER BY store DESC ')

plat = ('select p.platform, count(distinct p.user_pseudo_id) as volume '
    'from (SELECT platform,user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "ecommerce_purchase" and date(TIMESTAMP_MICROS(event_timestamp+14400000000)) = @dates) as p '
    'inner join '
    '(SELECT user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "first_open" and date(TIMESTAMP_MICROS(event_timestamp+14400000000)) = @dates) as f on p.user_pseudo_id = f.user_pseudo_id '
    'group by p.platform '
    'order by platform')

cou = ('select p.country, count(distinct p.user_pseudo_id) as volume '
    'from (SELECT geo.country,user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "ecommerce_purchase" and date(TIMESTAMP_MICROS(event_timestamp+14400000000)) = @dates) as p '
    'inner join '
    '(SELECT user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "first_open" and date(TIMESTAMP_MICROS(event_timestamp+14400000000)) = @dates) as f on p.user_pseudo_id = f.user_pseudo_id '
    'group by p.country '
    'order by volume desc ')

cam = ('select p.campaign, count(distinct p.user_pseudo_id) as volume from '
    '(SELECT case when traffic_source.name is null or traffic_source.name ="(direct)" then "organic" else traffic_source.name end as campaign, user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "ecommerce_purchase" and date(TIMESTAMP_MICROS(event_timestamp+14400000000)) = @dates) as p '
    'inner join '
    '(SELECT user_pseudo_id '
    'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
    'WHERE event_name = "first_open" and date(TIMESTAMP_MICROS(event_timestamp+14400000000)) = @dates) as f on p.user_pseudo_id = f.user_pseudo_id '
    'group by p.campaign '
    'order by volume desc ')

def login(func, m):
    for user in users:
        if m.from_user.username != user:
            continue
        else:
            global question  
            markup = telebot.types.ReplyKeyboardMarkup()
            markup.row('вчера', 'позавчера')
            markup.row(str(date.today()-timedelta(3)), str(date.today()-timedelta(4)))
            question = bot.send_message(m.chat.id, '{}, введите дату.'.format(m.from_user.first_name), reply_markup=markup)
            bot.register_next_step_handler(question, func)
            break
    else:
        start_menu = bot.send_message(m.chat.id, '{}, вы не зарегистрированы'.format(m.from_user.first_name))

def query(q,m,n):
    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/v_rusakevich/Documents/Виджеты power bi/Yolla-d505c9833f92.json'
        client = bigquery.Client()
        QUERY = (q)
        m.text = m.text.lower()
        if m.text == 'вчера':
            dates = str(date.today()-timedelta(1)) 
        elif m.text == 'позавчера':
            dates = str(date.today()-timedelta(2))
        elif m.text[2] == '-':
            dates = m.text[6:]+m.text[2:5]+'-'+m.text[:2]
        elif len(m.text) == 8 and m.text[0] == '2':
            dates = m.text[:4]+'-'+m.text[4:6]+'-'+m.text[6:]
        elif len(m.text) == 8 and m.text[4] == '2':
            dates = m.text[4:]+'-'+m.text[2:4]+'-'+m.text[:2]
        else:
            dates = m.text
        param = bigquery.ScalarQueryParameter('dates', 'STRING', dates)
        job_config = bigquery.QueryJobConfig()
        job_config.query_parameters = [param]
        query_job = client.query(QUERY, job_config=job_config) 
        rows = query_job.result()
        bot.send_message(m.chat.id, '*Данные за {} по {}*'.format(dates,n), parse_mode='Markdown')
        tex = []
        for row in rows:
            T=''
            L = len(row)
            while L>0:
                T = str(row[L-1])+' - '+T
                L-=1
            T= T[:-2]
            tex.append(T)
            #tex.append('{} - {}'.format(row[0], row[1]))
            #print(len(row))
            #bot.send_message(m.chat.id, '{} - {}'.format(row[0], row[1]))
            #print(row[0])
        mes = '\n'.join(tex)
        bot.send_message(m.chat.id, mes)
        bot.send_message(m.chat.id, '_Готово_', parse_mode='Markdown')
    except Exception as er:
        print(er) 
        bot.send_message(m.chat.id, 'Ошибка. Попробуйте снова.')


@bot.message_handler(commands=['country'])
def start(message):
    login(country, message)
    
@bot.message_handler(commands=['platform'])
def start(message):
    login(platform, message)

@bot.message_handler(commands=['campaign'])
def start(message):
    login(campaign, message)

@bot.message_handler(commands=['googleplay'])
def start(message):
    login(googleplay, message)


@bot.message_handler(commands=['start'])
def start(message):
    for user in users:
        if message.from_user.username != user:
            continue
        else:
            bot.send_message(message.chat.id, 'Команды:\n /campaign - данные платящих по кампаниям'
            ' \n /country - данные платящих по странам\n /platform - данные платящих по платформам'
            ' \n /googleplay - данные по странам из Google Play - Просмотры-Установившие приложение-конверсия,%-1 день')
            break
    else:
        start_menu = bot.send_message(message.chat.id, '{}, вы не зарегистрированы'.format(message.from_user.first_name))



def country(message):
    query(cou, message, 'странам')

def platform(message):
    query(plat, message, 'платформам')

def campaign(message):
    query(cam, message, 'кампаниям')

def googleplay(message):
    query(gplay, message, 'google play')


#bot.polling(none_stop=True)
while True:
    try:
        bot.infinity_polling(none_stop=True)

    except Exception as e:
        print(e)  # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)

