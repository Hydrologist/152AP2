import simpy
def car(env):
	while True:
		print('Start parking at ', env.now)
		yield env.timeout(5)
		print('Start driving at ', env.now)
		yield env.timeout(1)

env = simpy.Environment()
env.process(car(env))
env.process(car(env))
env.run(until=20)