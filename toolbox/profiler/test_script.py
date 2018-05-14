from time import sleep
from toolbox.profiler import Profiler

def fibonacci(number):
	if number is 0 or number is 1:
		return 1
	return fibonacci(number-1) + fibonacci(number-2)

with Profiler():
	fibonacci(30)
