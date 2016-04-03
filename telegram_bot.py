#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and run until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater
from ptt_board import ptt_board
import parser
import vars
import logging

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

command_handler = {}
type_handler = {}
updater = None
board = {}

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    pass
    #bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=\
        'The following keywords entered will be detected:\n' +\
        ', '.join(vars.cat_list) +  '\n' +\
        ', '.join(vars.girl_list))

def command(bot, update):
    global command_handler
    s = update.message.text.split(' ')
    if s[1] in command_handler.keys():
        command_handler[s[1]](bot, update)

def echo(bot, update):
    global type_handler
    t = parser.get_message_type(update.message.text)
    if t in type_handler.keys():
        image_url = type_handler[t]()
        bot.sendPhoto(update.message.chat_id, photo = image_url)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def get_ptt_image(type_str):
    current_board = None
    global board
    if type_str in board:
        current_board = board[type_str]

    if not current_board:
        current_board = ptt_board(type_str)
        board[type_str] = current_board

    image_url = None
    article = None
    while not image_url:
        article = current_board.get_random_page().get_random_article(lower_bound = vars.lower_bound_dict[type_str])
        if article:
            image_url = article.get_random_image()
    print('image: ' + image_url)
    return image_url

def main():
    global command_handler
    command_handler = {'help' : help}
    global type_handler
    type_handler = {\
        vars.cat_str : lambda: get_ptt_image(vars.cat_str),\
        vars.girl_str : lambda: get_ptt_image(vars.girl_str)
    }

    # Create the EventHandler and pass it your bot's token.
    global updater
    updater = Updater("202654459:AAH1GTl4OE55CzNXwzXZ5Qqj3C7onFa-syA")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("yomao", command)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()