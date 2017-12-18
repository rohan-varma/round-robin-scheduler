from collections import deque
import threading
from threading import Thread
from time import sleep
from datetime import datetime
import random

def my_xrange(i, job_id):
	cur = 0
	while cur < i: 
		print("job {} running".format(job_id))
		yield cur, job_id
		cur+=1


class Job(object):
	def __init__(self, job_func, kwargs, job_priority, job_id = None):
		self.job = job_func(**kwargs)
		self.kwargs = kwargs
		self.priority = job_priority
		self.id = job_id if job_id else random.randint(1, 1000)
		self.num_times_run = 0
		self.time_taken = 0

	def run(self):
		print('running job with id {} and priority {}'.format(self.id, self.priority))
		now = datetime.now()
		next(self.job)
		self.time_taken += datetime.now() - now
		self.num_times_run+=1

class Scheduler(object):
	def __init__(self, tasks):
		self.waiting_tasks = deque(tasks)

	def run_scheduled_jobs(self):
		# while there are jobs to process
		while len(self.waiting_tasks) > 0:
			# pick a job from the top
			current_task = self.waiting_tasks.popleft()
			finished = False
			# run the task until it yields
			try:
				sleep(1)
				current_task.run()
			except StopIteration:
				# if we're here that means the task is done, so don't add it back to the list
				finished = True
			if not finished:
				self.waiting_tasks.append(current_task)

	def add_jobs(self, num_jobs):
		print('adding {} jobs'.format(num_jobs))
		priorites = [1, 2, 3, 4]
		new_jobs = [Job(my_xrange, {'i': 50, 'job_id': 6 + i},
			job_priority=priorites[random.randint(0, len(priorites)-1)]) for i in range(num_jobs)]
		for job in new_jobs:
			print('adding a job with id {} and priority {}'.format(job.id, job.priority))
			self.waiting_tasks.append(job)
			sleep(1)


if __name__ == '__main__':
	generator = my_xrange(1, 1)
	try:
		while True:
			print(next(generator))
	except StopIteration:
		print("done")
	priorites = [1, 2, 3, 4]
	tasks = [Job(my_xrange, {'i': 5, 'job_id': i},
		job_priority=priorites[random.randint(0, len(priorites)-1)]) for i in range(5)]
	scheduler = Scheduler(tasks)
	task_runner = Thread(target = scheduler.run_scheduled_jobs, name = 'task-runner')
	job_adder = Thread(target = scheduler.add_jobs, name = 'job-adder', kwargs ={'num_jobs': 10})
	threads = [task_runner, job_adder]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
