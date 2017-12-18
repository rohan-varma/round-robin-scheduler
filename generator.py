from collections import deque
import threading
from threading import Thread
from time import sleep

def my_xrange(i, job_id):
	cur = 0
	while cur < i: 
		print("job {} running".format(job_id))
		yield cur, job_id
		cur+=1


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
				next(current_task)
			except StopIteration:
				# if we're here that means the task is done, so don't add it back to the list
				finished = True
			if not finished:
				self.waiting_tasks.append(current_task)

	def add_jobs(self, num_jobs):
		print('adding {} jobs'.format(num_jobs))
		new_jobs = [my_xrange(50, 6 + i) for i in range(num_jobs)]
		for job in new_jobs:
			print('adding a job')
			self.waiting_tasks.append(job)
			sleep(1)







if __name__ == '__main__':
	generator = my_xrange(1, 1)
	try:
		while True:
			print(next(generator))
	except StopIteration:
		print("done")

	tasks = [my_xrange(5, i) for i in range(5)]
	scheduler = Scheduler(tasks)
	task_runner = Thread(target = scheduler.run_scheduled_jobs, name = 'task-runner')
	job_adder = Thread(target = scheduler.add_jobs, name = 'job-adder', kwargs ={'num_jobs': 10})
	threads = [task_runner, job_adder]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
