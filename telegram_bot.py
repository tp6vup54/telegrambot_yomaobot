import telebot
import logging
import flask
import configparser
from ptt_board import ptt_board
from message_parser import get_message_type
from vars import vars
from util import console_out

config = configparser.ConfigParser()
config.sections()
config.read('yomaobot.conf')

API_TOKEN = config['DEFAULTS']['bot_token']

WEBHOOK_HOST = config['DEFAULTS']['url']
WEBHOOK_PORT = int(config['DEFAULTS']['nginx_port'])
WEBHOOK_PORT_PROXY = int(config['DEFAULTS']['proxy_port'])
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % (API_TOKEN)

updater = None
board = {}

command_handler = {'help' : help}
type_handler = {\
    vars.cat_str : lambda: get_ptt_image(vars.cat_str),\
    vars.girl_str : lambda: get_ptt_image(vars.girl_str)
}

def get_ptt_image(type_str):
    current_board = None
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
    console_out('image: ' + image_url)
    return image_url

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data()
        try:
            json_string = json_string.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
        except:
            console_out('get except')
            console_out(json_string)
            return ''
        bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)

# Handle '/yomao'
@bot.message_handler(commands=['yomao'])
def parse_command(message):
    console_out('get command')
    global command_handler
    m = message.text.split(' ')
    if len(m) > 2 and m[1].lower() in command_handler:
        command_handler[m[1].lower()](message)

def help(message):
    console_out('help')
    bot.reply_to(message, 'The following keywords entered will be detected:\n' +\
        ', '.join(vars.cat_list) +  '\n' +\
        ', '.join(vars.girl_list))

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    console_out('>>echo_message: ' + message.text)
    global type_handler
    t = get_message_type(message.text.lower())
    if t in type_handler:
        image_url = type_handler[t]()
        bot.reply_to(message, image_url)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
# start flask server

app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT_PROXY,
        debug=True)
