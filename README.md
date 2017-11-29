### round-robin-scheduler

Basic implementation of round robin scheduling to understand the algorithm as well as generators in Python. 

Jobs are represented as generators. A job is considered "running" when `next()` is called on the generator, and then the generator will run until it yields a value. 

A job is considered finsihed when the generator raises a `StopIteration`, indicating that it has no more values to yield. 

The algorithm is pretty basic - it considers the list of tasks as a set of waiting tasks. In each iteration, the top task is taken, ran (by calling the `next` method), and if a `StopIteration` is excepted, then it is not added back to the list of waiting tasks (else it is).

Additional work: 

1) Implement spawning jobs - adding additional jobs to the list of waiting jobs while other jobs are running (requires multiple threads)
2) Implement `fork()` and `wait()` to simulate child processes
3) Implement priorities for jobs, and priority boosting like the MLFQ algorithm [here](https://en.wikipedia.org/wiki/Multilevel_feedback_queue)
