import telebot
import logging
import os
import flask
import configparser
import logging
import logging.config
import time
from ptt_board import ptt_board
from message_parser import get_message_type
from vars import vars

config = configparser.ConfigParser()
config.sections()
config.read('yomaobot.conf')

API_TOKEN = config['DEFAULTS']['bot_token']

WEBHOOK_HOST = config['DEFAULTS']['url']
WEBHOOK_PORT = int(config['DEFAULTS']['port_webhook'])
WEBHOOK_PORT_PROXY = int(config['DEFAULTS']['port_proxy'])
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % (API_TOKEN)

updater = None
board = {}

def my_help(message):
    logging.info('help')
    bot.reply_to(message, 'The following keywords entered will be detected:\n' +\
        ', '.join(vars.cat_list) +  '\n' +\
        ', '.join(vars.girl_list))

command_handler = {'help' : my_help}
type_handler = {
    vars.cat_str : lambda: get_ptt_image(vars.cat_str),
    vars.girl_str : lambda: get_ptt_image(vars.girl_str),
}

def init_logger():
    """
    Init logger. Default use INFO level. If 'DEBUG' is '1' in env use DEBUG level.
    :return:
    """
    logging.config.fileConfig("./logging.conf")
    root = logging.getLogger()
    level = logging.INFO
    if os.getenv("DEBUG") == '1':
        level = logging.DEBUG
    root.setLevel(level)

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
        logging.info('image: %s.' % image_url)
    return image_url

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

init_logger()
logging.info('Init bot use token. %s' % API_TOKEN)
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
            logging.info('get except, %s.' % json_string)
            return ''
        if update.message:
            bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


# Handle '/yomao'
@bot.message_handler(commands=['yomao'])
def parse_command(message):
    logging.info('get command, %s.' % message.text)
    bot.send_message(config['DEFAULTS']['my_chat_id'], 'test')
    global command_handler
    m = message.text.split(' ')
    if len(m) >= 2 and m[1].lower() in command_handler:
        command_handler[m[1].lower()](message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    logging.info('echo message: %s.' % message.text)
    global type_handler
    t = get_message_type(message.text.lower())
    if t in type_handler:
        image_url = type_handler[t]()
        bot.reply_to(message, image_url)


logging.info('remove previous webhook')
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(0.1)
logging.info('setting webhook with url: %s%s' % (WEBHOOK_URL_BASE, WEBHOOK_URL_PATH))
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open('/etc/ssl/bot_vps_yomao_xyz.pem', 'r'))
logging.info('start webhook with host %s and port %s.' % (WEBHOOK_LISTEN, WEBHOOK_PORT_PROXY))
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT_PROXY,
        debug=True)
