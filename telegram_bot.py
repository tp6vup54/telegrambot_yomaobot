import telebot
from ptt_board import ptt_board
from message_parser import get_message_type
import vars

command_handler = {}
type_handler = {}
updater = None
board = {}

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

bot = telebot.TeleBot('202654459:AAH1GTl4OE55CzNXwzXZ5Qqj3C7onFa-syA')

# Handle '/yomao'
@bot.message_handler(commands=['yomao'])
def parse_command(message):
    global command_handler
    if message.text.split(' ')[1].lower() in command_handler:
        command_handler[message.text.split(' ')[1].lower()](message)

def help(message):
    bot.reply_to(message, 'The following keywords entered will be detected:\n' +\
        ', '.join(vars.cat_list) +  '\n' +\
        ', '.join(vars.girl_list))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    print('>>echo_message')
    global type_handler
    t = get_message_type(message.text.lower())
    if t in type_handler.keys():
        image_url = type_handler[t]()
        #bot.sendPhoto(update.message.chat_id, photo = image_url)
        bot.reply_to(message, image_url)

def main():
    global command_handler
    command_handler = {'help' : help}
    global type_handler
    type_handler = {\
        vars.cat_str : lambda: get_ptt_image(vars.cat_str),\
        vars.girl_str : lambda: get_ptt_image(vars.girl_str)
    }
    global bot
    bot.polling()
if __name__ == '__main__':
    main()