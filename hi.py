import itertools
import random
import math
import simpy
env = simpy.Environment()
res = simpy.Resource(env, capacity=1)

def check_resource(env, res):
	while True:
		#print("Queue size: ", len(res.queue))
		#print("Time: ", env.now)
		yield env.timeout(2)
		print(env.now)

def use_resource(env, res):
	while True:
		request = res.request()
		print("Queue Size in user after request: ", len(res.queue))
		print("Before yield: ", env.now)
		print("After yield: ", env.now)
		res.release(request)
		print("Queue Size in user after release: ", len(res.queue))
		print("Doing something at", env.now)
		yield env.timeout(1)
#env.process(check_resource(env, res))
#env.process(use_resource(env, res))
for i in range(1,9):
	env.process(check_resource(env, res))
env.process(use_resource(env, res))

env.run(until=10)