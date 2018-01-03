from flask import Flask, request, send_file
import telegram
from telegram_bot import *

app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	tele_bot.update(update)
	return 'ok'

if __name__ == "__main__":
	bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
	tele_bot = TelegramBot.start(bot).proxy()

	app.run()