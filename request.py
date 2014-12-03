import random
import simpy
import math
SIM_TIME = 100

env= simpy.Environment()
server = simpy.Resource(env, capacity=1)
def server_time(server, env):
	while True:
		yield env.timeout(10)
		print("Server Time is ", env.now)
		request = server.request()
def host_time(server, env):
	while True:
		yield env.timeout(5)
		print("Host Time is ", env.now)
		print("Queue is ",len(server.queue))

	
env.process(server_time(server, env))
env.process(host_time(server, env))
env.run(until=SIM_TIME)
