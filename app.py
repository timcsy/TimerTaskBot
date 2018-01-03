from config import *
import sys
from io import BytesIO
import telegram
from flask import Flask, request, send_file
from fsm import *
from crossbot import *
from schedule import *
from message import *

app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
task = MainTask(bot)

def _set_webhook():
    status = bot.set_webhook(TELEGRAM_WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(TELEGRAM_WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print(update)
    task.receive(Message('Telegram', update))
    # machine.advance(bot, update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    task.start()
    app.run(threaded=True)