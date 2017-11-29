from collections import deque

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
				next(current_task)
			except StopIteration:
				# if we're here that means the task is done, so don't add it back to the list
				finished = True
			if not finished:
				self.waiting_tasks.append(current_task)





if __name__ == '__main__':
	generator = my_xrange(1, 1)
	try:
		while True:
			print(next(generator))
	except StopIteration:
		print("done")

	tasks = [my_xrange(5, i) for i in range(5)]
	scheduler = Scheduler(tasks)
	scheduler.run_scheduled_jobs()

	