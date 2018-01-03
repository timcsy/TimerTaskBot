import threading
import heapq
import time
import pykka
from fsm import TocMachine

class Task:
	def __init__(self, bot, interval):
		self.bot = bot
		self.interval = interval
		self.canceled = False
		
	def start(self):
		self.bot.send_text("Task " + str(self.interval) + ' expired')

	def next_time(self):
		return self.interval

class Scheduler:
	def __init__(self):
		self.tasks = []
		self.queue = []
		self.thread = None
		
	def add(self, task):
		self.tasks.append(task)
		self.push(task)

	def cancel(self, task):
		task.canceled = True
	
	def list_tasks(self):
		return self.tasks

	def clear(self):
		self.tasks.clear()
		self.queue.clear()

	def run(self):
		while len(self.queue) > 0 and self.queue[0][1].canceled == True:
			heapq.heappop(self.queue)
		if len(self.queue) > 0:
			timestamp, task = heapq.heappop(self.queue)
			self.next()
			task.start()
			if task.canceled != True:
				self.push(task)
	
	def push(self, task):
		now = time.time()
		next_time = task.next_time()
		heapq.heappush(self.queue, (now + next_time, task))
		self.next()
	
	def next(self):
		if self.thread is None:
			self.thread.cancel()
		if len(self.queue) > 0:
			now = time.time()
			next_time = 0
			if self.queue[0][0] > now:
				next_time = self.queue[0][0] - now
			self.thread = threading.Timer(next_time, self.run)
			self.thread.start()


class ScheduleActor(pykka.ThreadingActor):
	def __init__(self, bot):
		super(ScheduleActor, self).__init__()
		self.bot = bot
		self.scheduler = Scheduler()
		self.machine = TocMachine(
			states=[
				'instruction',
				'schedule',
				'add',
				'interval',
				'cancel',
				'num'
				'list',
				'restart'
			],
			transitions=[
				['schedule', 'instruction' , 'schedule'],
				['add', 'schedule' , 'add'],
				['input', 'add' , 'interval'],
				['go_back', 'interval' , 'schedule'],
				['cancel', 'schedule' , 'cancel'],
				['input', 'cancel' , 'num'],
				['go_back', 'num' , 'schedule'],
				['list', 'schedule' , 'list'],
				['go_back', 'list' , 'schedule'],
				['restart', 'schedule' , 'instruction']
			],
			initial='instruction',
			auto_transitions=False,
			show_conditions=True,
    )
		self.bot.send_text('Welcome to Scheduler,\ntype the following words,\nadd: to add a task\ncancel: to cancel a task\nlist: list tasks')
		self.state = 'start'

	def on_receive(self, message):
		msg = message['msg']
		if self.state == 'schedule':
			if msg == 'add':
				self.state = 'add'
				self.bot.send_text('enter interval: ')
			elif msg == 'list':
				list = self.scheduler.list_tasks()
				s = 'tasks:\n'
				for i in range(len(list)):
					if list[i].canceled == False:
						s += str(i) + ': ' + str(list[i].interval) + '\n'
				self.bot.send_text(s)
			elif msg == 'cancel':
				self.state = 'cancel'
				self.bot.send_text('Please enter the task number: ')
			elif msg == 'restart':
				self.scheduler.clear()
				self.bot.send_text('Restart')
		elif self.state == 'add':
			interval = int(msg)
			self.scheduler.add(Task(self.bot, interval))
			self.state = 'schedule'
		elif self.state == 'cancel':
			task_num = int(msg)
			self.scheduler.cancel(self.scheduler.tasks[task_num])
			self.state = 'schedule'