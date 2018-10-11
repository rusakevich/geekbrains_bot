import requests
import telebot
import urllib.request
import zipfile2
import os

def remove_stickers():
    if os.path.exists('stickers.zip'):
        os.remove('stickers.zip')
numbers_file = 1
emoji = []
TOKEN = '660998626:AAHgAzbMgxUhhLA8dlcb7u192Az5FCeWnpM'
bot = telebot.TeleBot(TOKEN)
BASE_URL = 'https://api.telegram.org/bot660998626:AAHgAzbMgxUhhLA8dlcb7u192Az5FCeWnpM/'
BASE_URL_FILE = 'https://api.telegram.org/file/bot660998626:AAHgAzbMgxUhhLA8dlcb7u192Az5FCeWnpM/'




@bot.message_handler(commands=['start'])
def start(message):
    remove_stickers()   
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('STOP')
    bot.send_message(message.chat.id, '{}, здравствуйте. Это бот, который присылает архив стикеров обратно. Пришлите стикеров'.format(message.from_user.first_name),  reply_markup=markup)



@bot.message_handler(content_types=['sticker'])
def begin(message):
    remove_stickers()
    r = message.sticker
    global numbers_file, emoji
    param = {'file_id':r.file_id}
    fh = requests.post(BASE_URL+'getFile',data=param).json()['result']['file_path']
    sticker = urllib.request.urlopen(BASE_URL_FILE+fh).read()
    out = open('sticker'+str(numbers_file)+'.webp', "wb")
    out.write(sticker)
    out.close
    numbers_file += 1
    emoji.append(r.emoji)


@bot.message_handler(func=lambda message: message.text == "STOP")
def send_something(message):
    try:
        remove_stickers()
        global numbers_file, emoji
        b=numbers_file-1
        while numbers_file-1:
            stickers_zip = zipfile2.ZipFile('stickers.zip', 'a')
            stickers_zip.write('sticker'+str(numbers_file-1)+'.webp', compress_type=zipfile2.ZIP_DEFLATED)
            stickers_zip.close()
            numbers_file -= 1
        doc = open('stickers.zip', 'rb')
        bot.send_document(message.chat.id, doc)
        bot.send_message(message.chat.id, emoji if len(emoji)==1 else ' '.join(emoji))
        emoji = []
        while b:
            os.remove('sticker'+str(b)+'.webp')
            b=b-1
    except:
        bot.send_message(message.chat.id, '{}, стикеры отсутствуют. Пришилите стикеры'.format(message.from_user.first_name))





while True:
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
