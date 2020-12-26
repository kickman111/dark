from telegram import Bot
from telegram import Update
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


from config import BOT_TOKEN
from config import API_URL

# API_link = 'https://api.telegram.org/bot1457675734:AAG6gVaX536-WmOrGA-gDe6wVUSFbNlaljw'

def do_start(bot: Bot, update: Update):
    # функция для текста \start (не забываем подключить handler и dispatcher
    bot.send_message(chat_id=update.message.chat_id, text='Привет, дорогой друг!\n'
                                                          'Ты залетел в магазин волшебства, '
                                                          'мы поможем тебе хорошо провести время')

def do_help(bot: Bot, update: Update):
    # функция для текста \help
    bot.send_message(chat_id=update.message.chat_id, text='Текст в меню хелпа\n')

def do_town(bot: Bot, update: Update):
    # функция для текста \town
    bot.send_message(chat_id=update.message.chat_id, text='Москва\nПитер')

def do_products(bot: Bot, update: Update):
    # функция для текста \products
    bot.send_message(chat_id=update.message.chat_id, text='Фен\nМДМА\nДМА\nГрибы\nЛСД\nМефедрон')

def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text_echo = update.message.text
    text = "Ваш ID = {}\n{}".format(chat_id, text_echo)
    bot.send_message(chat_id=update.message.chat_id, text=text,)
    print(text)

def main():
    bot = Bot(token=BOT_TOKEN,)
    updater = Updater(bot=bot,)
    start_handler = CommandHandler('start', do_start)
    help_handler = CommandHandler('help', do_help)
    town_handler = CommandHandler('town', do_town)
    products_handler = CommandHandler('products', do_products)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(town_handler)
    updater.dispatcher.add_handler(products_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# updates = requests.get(API_link + '/getUpdates?offset-1').json()

# message = updates['result'][0]['message']
# chat_id = message['from']['id']
# text = message['text']

# sent_message = requests.get(API_link + f'/sendMessage?chat_id{chat_id}& \
#                                        text=Приветствуем тебя в нашем магазине, дорогой друг! Ты написал {text}')
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
