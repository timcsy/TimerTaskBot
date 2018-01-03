from config import *
import pykka
import sys
from schedule import ScheduleActor

class TelegramBot(pykka.ThreadingActor):
	def __init__(self, bot):
		super(TelegramBot, self).__init__()
		self.bot = bot
		self.chats = {}
		self._set_webhook()

	def _set_webhook(self):
		status = self.bot.set_webhook(TELEGRAM_WEBHOOK_URL)
		if not status:
			print('Webhook setup failed')
			sys.exit(1)
		else:
			print('Your webhook URL has been set to "{}"'.format(TELEGRAM_WEBHOOK_URL))
	
	def update(self, update):
		chat_id = update.message.chat.id
		if not chat_id in self.chats:
			self.chats[chat_id] = TelegramChatActor.start(self, chat_id).proxy()
		self.chats[chat_id].update(update).get()
	
	def send_text(self, chat_id, message):
		self.bot.send_message(chat_id, message)
	
	def send_photo(self, chat_id, photo):
		self.bot.send_photo(chat_id, photo)


class TelegramChatActor(pykka.ThreadingActor):
	def __init__(self, tele_bot, id):
		super(TelegramChatActor, self).__init__()
		self.tele_bot = tele_bot
		self.id = id
		self.state = 'start'
	
	def update(self, update):
		text = update.message.text.replace("/", "").lower()
		if self.state == 'start':
			self.schedule_actor = ScheduleActor.start(self)
			self.state = 'schedule'
		elif self.state == 'schedule':
			self.schedule_actor.tell({'msg': text})

	def send_text(self, message):
		self.tele_bot.send_text(self.id, message)

	def send_photo(self, photo):
		self.tele_bot.send_photo(self.id, photo)